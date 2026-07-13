from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn

from .config import MoEConfig
from .mlp import Expert
from .routing import NormalizedSigmoidTopKRouter, RouterOutput


@dataclass
class TokenDispatch:
    hidden_states: torch.Tensor
    token_indices: torch.Tensor
    expert_indices: torch.Tensor
    weights: torch.Tensor
    counts: torch.Tensor


def dispatch_tokens(
    hidden_states: torch.Tensor,
    expert_indices: torch.Tensor,
    expert_weights: torch.Tensor,
    num_experts: int,
) -> TokenDispatch:
    """Sort token-expert assignments into contiguous per-expert batches."""
    if hidden_states.ndim != 2:
        raise ValueError("hidden_states must have shape [tokens, hidden]")
    if expert_indices.shape != expert_weights.shape or expert_indices.ndim != 2:
        raise ValueError("router indices and weights must have shape [tokens, top_k]")
    top_k = expert_indices.shape[1]
    token_indices = torch.arange(
        hidden_states.shape[0], device=hidden_states.device
    ).repeat_interleave(top_k)
    flat_experts = expert_indices.reshape(-1)
    flat_weights = expert_weights.reshape(-1)
    order = torch.argsort(flat_experts, stable=True)
    sorted_tokens = token_indices.index_select(0, order)
    sorted_experts = flat_experts.index_select(0, order)
    counts = torch.bincount(sorted_experts, minlength=num_experts)
    return TokenDispatch(
        hidden_states=hidden_states.index_select(0, sorted_tokens),
        token_indices=sorted_tokens,
        expert_indices=sorted_experts,
        weights=flat_weights.index_select(0, order),
        counts=counts,
    )


def scatter_expert_outputs(
    expert_outputs: torch.Tensor,
    dispatch: TokenDispatch,
    num_tokens: int,
) -> torch.Tensor:
    """Weight and sum expert outputs back into original token order."""
    result = expert_outputs.new_zeros((num_tokens, expert_outputs.shape[-1]))
    weighted = expert_outputs * dispatch.weights.to(expert_outputs.dtype).unsqueeze(-1)
    result.index_add_(0, dispatch.token_indices, weighted)
    return result


class MoELayer(nn.Module):
    def __init__(self, hidden_size: int, config: MoEConfig) -> None:
        super().__init__()
        self.config = config
        self.router = NormalizedSigmoidTopKRouter(
            hidden_size,
            config.routed_experts,
            config.experts_per_token,
            bias_update_rate=config.router_bias_update_rate,
        )
        self.routed_experts = nn.ModuleList(
            Expert(hidden_size, config.expert_intermediate_size)
            for _ in range(config.routed_experts)
        )
        self.shared_experts = nn.ModuleList(
            Expert(hidden_size, config.expert_intermediate_size)
            for _ in range(config.shared_experts)
        )

    def forward(
        self, hidden_states: torch.Tensor
    ) -> tuple[torch.Tensor, RouterOutput]:
        original_shape = hidden_states.shape
        flat_states = hidden_states.reshape(-1, original_shape[-1])
        router_output = self.router(flat_states)
        dispatch = dispatch_tokens(
            flat_states,
            router_output.expert_indices,
            router_output.expert_weights,
            self.config.routed_experts,
        )

        routed_chunks: list[torch.Tensor] = []
        offset = 0
        for expert, count_tensor in zip(self.routed_experts, dispatch.counts):
            count = int(count_tensor.item())
            chunk = dispatch.hidden_states[offset : offset + count]
            routed_chunks.append(expert(chunk))
            offset += count
        routed = torch.cat(routed_chunks, dim=0)
        combined = scatter_expert_outputs(routed, dispatch, flat_states.shape[0])

        for shared_expert in self.shared_experts:
            combined = combined + shared_expert(flat_states)
        return combined.view(original_shape), router_output

    @torch.no_grad()
    def update_expert_bias(self, expert_counts: torch.Tensor) -> torch.Tensor:
        return self.router.update_expert_bias(expert_counts)
