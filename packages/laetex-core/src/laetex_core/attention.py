from __future__ import annotations

from typing import TypeAlias

import torch
from torch import nn

from .config import AttentionConfig
from .rotary import RotaryEmbedding, apply_rotary

KVCache: TypeAlias = tuple[torch.Tensor, torch.Tensor]


class GQACausalAttention(nn.Module):
    def __init__(
        self,
        hidden_size: int,
        config: AttentionConfig,
        *,
        mode: str | None = None,
    ) -> None:
        super().__init__()
        self.config = config
        self.mode = mode or config.mode
        if self.mode not in {"global", "local"}:
            raise ValueError("attention mode must be 'global' or 'local'")
        if self.mode == "local" and not config.sliding_window:
            raise ValueError("local attention requires a sliding window")

        self.query_heads = config.query_heads
        self.key_value_heads = config.key_value_heads
        self.head_dim = config.head_dim
        self.groups = config.query_heads // config.key_value_heads
        self.scale = config.head_dim**-0.5

        self.q_proj = nn.Linear(
            hidden_size, config.query_heads * config.head_dim, bias=config.qkv_bias
        )
        self.k_proj = nn.Linear(
            hidden_size, config.key_value_heads * config.head_dim, bias=config.qkv_bias
        )
        self.v_proj = nn.Linear(
            hidden_size, config.key_value_heads * config.head_dim, bias=config.qkv_bias
        )
        self.o_proj = nn.Linear(config.query_heads * config.head_dim, hidden_size, bias=False)
        self.rope = RotaryEmbedding(config.head_dim, config.rope_theta)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        past_key_value: KVCache | None = None,
        use_cache: bool = False,
    ) -> tuple[torch.Tensor, KVCache | None]:
        batch_size, query_length, _ = hidden_states.shape
        past_length = 0 if past_key_value is None else past_key_value[0].shape[-2]

        query = self._shape(self.q_proj(hidden_states), self.query_heads)
        key = self._shape(self.k_proj(hidden_states), self.key_value_heads)
        value = self._shape(self.v_proj(hidden_states), self.key_value_heads)

        positions = torch.arange(
            past_length,
            past_length + query_length,
            device=hidden_states.device,
        ).expand(batch_size, -1)
        cosine, sine = self.rope(positions, dtype=query.dtype)
        query, key = apply_rotary(query, key, cosine, sine)

        if self.config.qk_norm:
            query = self._rms_normalize(query)
            key = self._rms_normalize(key)
        if past_key_value is not None:
            past_key, past_value = past_key_value
            if past_key.shape[:2] != (batch_size, self.key_value_heads):
                raise ValueError("past_key_value batch or KV-head dimensions do not match")
            key = torch.cat((past_key, key), dim=-2)
            value = torch.cat((past_value, value), dim=-2)
        present = (key, value) if use_cache else None

        expanded_key = key.repeat_interleave(self.groups, dim=1)
        expanded_value = value.repeat_interleave(self.groups, dim=1)
        scores = torch.matmul(query.float(), expanded_key.float().transpose(-1, -2))
        scores.mul_(self.scale)
        allowed = self._allowed_mask(
            batch_size=batch_size,
            query_length=query_length,
            key_length=key.shape[-2],
            past_length=past_length,
            device=hidden_states.device,
            attention_mask=attention_mask,
        )
        scores.masked_fill_(~allowed[:, None, :, :], -torch.inf)
        probabilities = torch.softmax(scores, dim=-1).to(expanded_value.dtype)
        context = torch.matmul(probabilities, expanded_value)
        context = context.transpose(1, 2).contiguous().view(batch_size, query_length, -1)
        return self.o_proj(context), present

    def _shape(self, values: torch.Tensor, heads: int) -> torch.Tensor:
        batch_size, sequence_length, _ = values.shape
        return values.view(batch_size, sequence_length, heads, self.head_dim).transpose(1, 2)

    def _allowed_mask(
        self,
        *,
        batch_size: int,
        query_length: int,
        key_length: int,
        past_length: int,
        device: torch.device,
        attention_mask: torch.Tensor | None,
    ) -> torch.Tensor:
        query_positions = torch.arange(
            past_length, past_length + query_length, device=device
        )[:, None]
        key_positions = torch.arange(key_length, device=device)[None, :]
        allowed = key_positions <= query_positions
        if self.mode == "local":
            allowed &= key_positions > query_positions - int(self.config.sliding_window)
        allowed = allowed[None, :, :].expand(batch_size, -1, -1)
        if attention_mask is not None:
            if attention_mask.ndim != 2 or attention_mask.shape[0] != batch_size:
                raise ValueError("attention_mask must have shape [batch, key_length]")
            if attention_mask.shape[1] == query_length and past_length:
                prefix = torch.ones(
                    batch_size,
                    past_length,
                    dtype=attention_mask.dtype,
                    device=device,
                )
                attention_mask = torch.cat((prefix, attention_mask), dim=1)
            if attention_mask.shape[1] != key_length:
                raise ValueError("attention_mask length must match current plus cached tokens")
            allowed &= attention_mask.to(device=device, dtype=torch.bool)[:, None, :]
        return allowed

    @staticmethod
    def _rms_normalize(values: torch.Tensor) -> torch.Tensor:
        dtype = values.dtype
        normalized = values.float() * torch.rsqrt(
            values.float().square().mean(dim=-1, keepdim=True) + 1e-6
        )
        return normalized.to(dtype)
