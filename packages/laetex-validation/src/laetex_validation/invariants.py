"""Cross-field invariants that JSON Schema cannot express clearly."""

from __future__ import annotations

from typing import Any, Mapping


def validate_invariants(config: Mapping[str, Any]) -> None:
    architecture = config["architecture"]
    attention = architecture["attention"]
    pattern = architecture["attention_pattern"]
    moe = architecture["moe"]
    expert_parallel_size = config["parallelism"]["expert_parallel_size"]

    errors: list[str] = []
    hidden_size = architecture["hidden_size"]
    query_width = attention["query_heads"] * attention["head_dim"]

    if query_width != hidden_size:
        errors.append("query_heads * head_dim must equal hidden_size")
    if attention["query_heads"] % attention["key_value_heads"] != 0:
        errors.append("query_heads must be divisible by key_value_heads")
    if moe["experts_per_token"] > moe["routed_experts"]:
        errors.append("experts_per_token cannot exceed routed_experts")
    if moe["routed_experts"] % 16 != 0:
        errors.append("routed_experts must be divisible by 16")
    if expert_parallel_size % 16 != 0:
        errors.append("expert_parallel_size must be divisible by 16")
    if moe["routed_experts"] % expert_parallel_size != 0:
        errors.append("routed_experts must be divisible by expert_parallel_size")

    cycle = pattern["local_layers"] + pattern["global_layers"]
    if architecture["num_layers"] % cycle != 0:
        errors.append("num_layers must be divisible by the local/global attention cycle")
    if pattern["local_window"] > pattern["max_context"]:
        errors.append("local_window cannot exceed max_context")

    if errors:
        raise ValueError("Invariant validation failed:\n" + "\n".join(errors))
