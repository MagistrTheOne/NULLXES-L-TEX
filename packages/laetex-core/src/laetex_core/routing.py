from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as functional
from torch import nn


@dataclass
class RouterOutput:
    expert_indices: torch.Tensor
    expert_weights: torch.Tensor
    expert_counts: torch.Tensor
    normalized_scores: torch.Tensor


class ExpertBiasState(nn.Module):
    """Checkpointable state for aux-loss-free load-balancing bias updates."""

    def __init__(self, num_experts: int, update_rate: float = 1e-3) -> None:
        super().__init__()
        self.update_rate = update_rate
        self.register_buffer("bias", torch.zeros(num_experts, dtype=torch.float32))
        self.register_buffer("last_counts", torch.zeros(num_experts, dtype=torch.float32))
        self.register_buffer("updates", torch.zeros((), dtype=torch.long))

    @torch.no_grad()
    def update(self, expert_counts: torch.Tensor) -> torch.Tensor:
        if expert_counts.shape != self.bias.shape:
            raise ValueError("expert_counts shape does not match router bias")
        counts = expert_counts.detach().to(device=self.bias.device, dtype=torch.float32)
        self.last_counts.copy_(counts)
        target = counts.mean()
        self.bias.add_(self.update_rate * torch.sign(target - counts))
        self.bias.sub_(self.bias.mean())
        self.updates.add_(1)
        return self.bias


class NormalizedSigmoidTopKRouter(nn.Module):
    def __init__(
        self,
        hidden_size: int,
        num_experts: int,
        top_k: int,
        *,
        bias_update_rate: float = 1e-3,
    ) -> None:
        super().__init__()
        if not 0 < top_k <= num_experts:
            raise ValueError("top_k must be in [1, num_experts]")
        self.num_experts = num_experts
        self.top_k = top_k
        self.gate = nn.Linear(hidden_size, num_experts, bias=False)
        self.bias_state = ExpertBiasState(num_experts, bias_update_rate)

    def forward(self, hidden_states: torch.Tensor) -> RouterOutput:
        logits = functional.linear(hidden_states.float(), self.gate.weight.float())
        sigmoid_scores = torch.sigmoid(logits)
        normalized_scores = sigmoid_scores / sigmoid_scores.sum(
            dim=-1, keepdim=True
        ).clamp_min(torch.finfo(torch.float32).eps)
        selection_scores = normalized_scores + self.bias_state.bias
        _, expert_indices = torch.topk(selection_scores, self.top_k, dim=-1)
        expert_weights = normalized_scores.gather(-1, expert_indices)
        expert_weights = expert_weights / expert_weights.sum(dim=-1, keepdim=True).clamp_min(
            torch.finfo(torch.float32).eps
        )
        expert_counts = torch.bincount(
            expert_indices.reshape(-1), minlength=self.num_experts
        ).to(torch.float32)
        return RouterOutput(
            expert_indices=expert_indices,
            expert_weights=expert_weights,
            expert_counts=expert_counts,
            normalized_scores=normalized_scores,
        )

    @torch.no_grad()
    def update_expert_bias(self, expert_counts: torch.Tensor) -> torch.Tensor:
        return self.bias_state.update(expert_counts)
