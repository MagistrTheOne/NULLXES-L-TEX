from __future__ import annotations

import torch
import torch.nn.functional as functional
from torch import nn


class SwiGLU(nn.Module):
    def forward(self, gate: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
        return functional.silu(gate) * value


class Expert(nn.Module):
    def __init__(self, hidden_size: int, intermediate_size: int) -> None:
        super().__init__()
        self.gate_proj = nn.Linear(hidden_size, intermediate_size, bias=False)
        self.up_proj = nn.Linear(hidden_size, intermediate_size, bias=False)
        self.down_proj = nn.Linear(intermediate_size, hidden_size, bias=False)
        self.activation = SwiGLU()

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        return self.down_proj(
            self.activation(self.gate_proj(hidden_states), self.up_proj(hidden_states))
        )
