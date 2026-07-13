"""Closed-form parameter accounting; this module never allocates model weights."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ParameterCount:
    total: int
    active: int
    components: dict[str, dict[str, int]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "active": self.active,
            "components": self.components,
        }


def count_parameters(config: Mapping[str, Any]) -> ParameterCount:
    """Count trainable parameters and parameters active for one token."""
    architecture = config["architecture"]
    attention = architecture["attention"]
    moe = architecture["moe"]

    vocab = architecture["vocab_size"]
    layers = architecture["num_layers"]
    hidden = architecture["hidden_size"]
    query_width = attention["query_heads"] * attention["head_dim"]
    kv_width = attention["key_value_heads"] * attention["head_dim"]
    expert_width = moe["expert_intermediate_size"]

    input_embeddings = vocab * hidden
    output_head = 0 if architecture["tie_word_embeddings"] else vocab * hidden

    attention_per_layer = (
        hidden * query_width
        + 2 * hidden * kv_width
        + query_width * hidden
    )
    qk_norm_per_layer = query_width + kv_width if attention["qk_norm"] else 0
    block_norms_per_layer = 2 * hidden
    final_norm = hidden

    router_per_layer = hidden * moe["routed_experts"]
    one_expert = 3 * hidden * expert_width
    experts_total_per_layer = (
        moe["routed_experts"] + moe["shared_experts"]
    ) * one_expert
    experts_active_per_layer = (
        moe["experts_per_token"] + moe["shared_experts"]
    ) * one_expert

    components = {
        "token_embeddings": {
            "total": input_embeddings,
            "active": input_embeddings,
        },
        "output_head": {"total": output_head, "active": output_head},
        "attention_projections": {
            "total": layers * attention_per_layer,
            "active": layers * attention_per_layer,
        },
        "attention_qk_norm": {
            "total": layers * qk_norm_per_layer,
            "active": layers * qk_norm_per_layer,
        },
        "block_norms": {
            "total": layers * block_norms_per_layer,
            "active": layers * block_norms_per_layer,
        },
        "final_norm": {"total": final_norm, "active": final_norm},
        "routers": {
            "total": layers * router_per_layer,
            "active": layers * router_per_layer,
        },
        "experts": {
            "total": layers * experts_total_per_layer,
            "active": layers * experts_active_per_layer,
        },
    }
    total = sum(component["total"] for component in components.values())
    active = sum(component["active"] for component in components.values())
    return ParameterCount(total=total, active=active, components=components)
