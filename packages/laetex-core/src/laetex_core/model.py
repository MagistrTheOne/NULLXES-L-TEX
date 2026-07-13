from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn.functional as functional
from torch import nn

from .attention import GQACausalAttention, KVCache
from .config import LaetexConfig
from .moe import MoELayer
from .norms import RMSNorm
from .routing import RouterOutput


@dataclass
class LaetexModelOutput:
    last_hidden_state: torch.Tensor
    past_key_values: tuple[KVCache, ...] | None
    router_outputs: tuple[RouterOutput, ...]


@dataclass
class LaetexCausalLMOutput:
    logits: torch.Tensor
    loss: torch.Tensor | None
    past_key_values: tuple[KVCache, ...] | None
    router_outputs: tuple[RouterOutput, ...]


class DecoderLayer(nn.Module):
    def __init__(self, config: LaetexConfig, layer_index: int) -> None:
        super().__init__()
        self.input_norm = RMSNorm(config.hidden_size, config.rms_norm_eps)
        self.attention = GQACausalAttention(
            config.hidden_size,
            config.attention,
            mode=config.attention_mode_for_layer(layer_index),
        )
        self.post_attention_norm = RMSNorm(config.hidden_size, config.rms_norm_eps)
        self.moe = MoELayer(config.hidden_size, config.moe)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        past_key_value: KVCache | None = None,
        use_cache: bool = False,
    ) -> tuple[torch.Tensor, KVCache | None, RouterOutput]:
        attention_output, present = self.attention(
            self.input_norm(hidden_states),
            attention_mask=attention_mask,
            past_key_value=past_key_value,
            use_cache=use_cache,
        )
        hidden_states = hidden_states + attention_output
        moe_output, router_output = self.moe(self.post_attention_norm(hidden_states))
        return hidden_states + moe_output, present, router_output


class LaetexModel(nn.Module):
    def __init__(
        self,
        config: LaetexConfig,
        *,
        allow_large_model: bool = False,
        max_materialized_parameters: int = 100_000_000,
    ) -> None:
        super().__init__()
        estimated = estimate_parameter_count(config)
        if not allow_large_model and estimated > max_materialized_parameters:
            raise ValueError(
                f"refusing to materialize an estimated {estimated:,}-parameter model; "
                "pass allow_large_model=True only in an intentional sharded environment"
            )
        self.config = config
        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size)
        self.layers = nn.ModuleList(
            DecoderLayer(config, layer_index) for layer_index in range(config.layers)
        )
        self.final_norm = RMSNorm(config.hidden_size, config.rms_norm_eps)
        self.apply(self._initialize_module)
        self._apply_residual_scaled_initialization()

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        past_key_values: tuple[KVCache, ...] | None = None,
        use_cache: bool = False,
    ) -> LaetexModelOutput:
        if input_ids.ndim != 2:
            raise ValueError("input_ids must have shape [batch, sequence]")
        if past_key_values is not None and len(past_key_values) != len(self.layers):
            raise ValueError("past_key_values must contain one entry per decoder layer")
        past_length = 0 if past_key_values is None else past_key_values[0][0].shape[-2]
        if past_length + input_ids.shape[1] > self.config.max_position_embeddings:
            raise ValueError("input exceeds max_position_embeddings")

        hidden_states = self.embed_tokens(input_ids)
        presents: list[KVCache] = []
        router_outputs: list[RouterOutput] = []
        for layer_index, layer in enumerate(self.layers):
            layer_past = None if past_key_values is None else past_key_values[layer_index]
            hidden_states, present, router_output = layer(
                hidden_states,
                attention_mask=attention_mask,
                past_key_value=layer_past,
                use_cache=use_cache,
            )
            if present is not None:
                presents.append(present)
            router_outputs.append(router_output)
        return LaetexModelOutput(
            last_hidden_state=self.final_norm(hidden_states),
            past_key_values=tuple(presents) if use_cache else None,
            router_outputs=tuple(router_outputs),
        )

    def _initialize_module(self, module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)

    def _apply_residual_scaled_initialization(self) -> None:
        residual_std = self.config.initializer_range / math.sqrt(2.0 * self.config.layers)
        for layer in self.layers:
            nn.init.normal_(layer.attention.o_proj.weight, mean=0.0, std=residual_std)
            for expert in (*layer.moe.routed_experts, *layer.moe.shared_experts):
                nn.init.normal_(expert.down_proj.weight, mean=0.0, std=residual_std)


class LaetexForCausalLM(nn.Module):
    def __init__(
        self,
        config: LaetexConfig,
        *,
        allow_large_model: bool = False,
        max_materialized_parameters: int = 100_000_000,
    ) -> None:
        super().__init__()
        self.config = config
        self.model = LaetexModel(
            config,
            allow_large_model=allow_large_model,
            max_materialized_parameters=max_materialized_parameters,
        )
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        if config.tie_word_embeddings:
            self.lm_head.weight = self.model.embed_tokens.weight
        else:
            nn.init.normal_(
                self.lm_head.weight, mean=0.0, std=config.initializer_range
            )

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        labels: torch.Tensor | None = None,
        past_key_values: tuple[KVCache, ...] | None = None,
        use_cache: bool = False,
    ) -> LaetexCausalLMOutput:
        outputs = self.model(
            input_ids,
            attention_mask=attention_mask,
            past_key_values=past_key_values,
            use_cache=use_cache,
        )
        logits = self.lm_head(outputs.last_hidden_state).float()
        loss = None
        if labels is not None:
            if labels.shape != input_ids.shape:
                raise ValueError("labels must have the same shape as input_ids")
            if labels.shape[1] < 2:
                raise ValueError("causal language-model loss requires at least two tokens")
            loss = functional.cross_entropy(
                logits[:, :-1, :].contiguous().view(-1, self.config.vocab_size),
                labels[:, 1:].contiguous().view(-1),
                ignore_index=-100,
            )
        return LaetexCausalLMOutput(
            logits=logits,
            loss=loss,
            past_key_values=outputs.past_key_values,
            router_outputs=outputs.router_outputs,
        )


def estimate_parameter_count(config: LaetexConfig) -> int:
    """Conservative materialized parameter estimate, including an LM head."""
    hidden = config.hidden_size
    attention = config.attention
    query_width = attention.query_heads * attention.head_dim
    kv_width = attention.key_value_heads * attention.head_dim
    attention_per_layer = hidden * (query_width + 2 * kv_width) + query_width * hidden
    if attention.qkv_bias:
        attention_per_layer += query_width + 2 * kv_width
    expert_count = config.moe.routed_experts + config.moe.shared_experts
    experts_per_layer = (
        expert_count * 3 * hidden * config.moe.expert_intermediate_size
    )
    router_per_layer = hidden * config.moe.routed_experts
    norms_per_layer = 2 * hidden
    embeddings = config.vocab_size * hidden
    lm_head = 0 if config.tie_word_embeddings else config.vocab_size * hidden
    return (
        embeddings
        + lm_head
        + hidden
        + config.layers
        * (attention_per_layer + experts_per_layer + router_per_layer + norms_per_layer)
    )
