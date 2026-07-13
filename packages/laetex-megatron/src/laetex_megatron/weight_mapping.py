from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


MAPPING_CONTRACT_VERSION = "laetex-megatron-weights/v1"


class WeightTransform(str, Enum):
    DIRECT = "direct"
    CONCAT_QKV = "concat_qkv"
    CONCAT_GATE_UP = "concat_gate_up"
    EXPERT_RESHARD = "expert_reshard"


@dataclass(frozen=True)
class WeightMapping:
    source_key: str
    target_key: str
    transform: WeightTransform
    component: str | None = None
    expert_index: int | None = None


_DIRECT_RULES = (
    (re.compile(r"^model\.embed_tokens\.weight$"), "embedding.word_embeddings.weight"),
    (re.compile(r"^lm_head\.weight$"), "output_layer.weight"),
    (re.compile(r"^model\.norm\.weight$"), "decoder.final_layernorm.weight"),
    (
        re.compile(r"^model\.layers\.(\d+)\.input_layernorm\.weight$"),
        "decoder.layers.{0}.input_layernorm.weight",
    ),
    (
        re.compile(r"^model\.layers\.(\d+)\.post_attention_layernorm\.weight$"),
        "decoder.layers.{0}.pre_mlp_layernorm.weight",
    ),
    (
        re.compile(r"^model\.layers\.(\d+)\.self_attn\.o_proj\.weight$"),
        "decoder.layers.{0}.self_attention.linear_proj.weight",
    ),
    (
        re.compile(r"^model\.layers\.(\d+)\.mlp\.gate\.weight$"),
        "decoder.layers.{0}.mlp.router.weight",
    ),
)

_QKV_RULE = re.compile(
    r"^model\.layers\.(\d+)\.self_attn\.(q_proj|k_proj|v_proj)\.weight$"
)
_EXPERT_RULE = re.compile(
    r"^model\.layers\.(\d+)\.mlp\.experts\.(\d+)\.(gate_proj|up_proj|down_proj)\.weight$"
)
_SHARED_RULE = re.compile(
    r"^model\.layers\.(\d+)\.mlp\.shared_expert\.(gate_proj|up_proj|down_proj)\.weight$"
)


def map_core_key(source_key: str) -> WeightMapping:
    """Map one canonical core key without touching tensors."""

    for pattern, target_template in _DIRECT_RULES:
        match = pattern.fullmatch(source_key)
        if match:
            return WeightMapping(
                source_key,
                target_template.format(*match.groups()),
                WeightTransform.DIRECT,
            )

    match = _QKV_RULE.fullmatch(source_key)
    if match:
        layer, projection = match.groups()
        return WeightMapping(
            source_key,
            f"decoder.layers.{layer}.self_attention.linear_qkv.weight",
            WeightTransform.CONCAT_QKV,
            component=projection.removesuffix("_proj"),
        )

    match = _EXPERT_RULE.fullmatch(source_key)
    if match:
        layer, expert, projection = match.groups()
        target_suffix = "linear_fc2.weight" if projection == "down_proj" else "linear_fc1.weight"
        transform = (
            WeightTransform.EXPERT_RESHARD
            if projection == "down_proj"
            else WeightTransform.CONCAT_GATE_UP
        )
        return WeightMapping(
            source_key,
            f"decoder.layers.{layer}.mlp.experts.local_experts.{expert}.{target_suffix}",
            transform,
            component=projection.removesuffix("_proj"),
            expert_index=int(expert),
        )

    match = _SHARED_RULE.fullmatch(source_key)
    if match:
        layer, projection = match.groups()
        target_suffix = "linear_fc2.weight" if projection == "down_proj" else "linear_fc1.weight"
        transform = (
            WeightTransform.DIRECT
            if projection == "down_proj"
            else WeightTransform.CONCAT_GATE_UP
        )
        return WeightMapping(
            source_key,
            f"decoder.layers.{layer}.mlp.shared_expert.{target_suffix}",
            transform,
            component=projection.removesuffix("_proj"),
        )

    raise KeyError(
        f"Unmapped core weight key under {MAPPING_CONTRACT_VERSION}: {source_key}"
    )


def plan_weight_mapping(source_keys: Iterable[str]) -> tuple[WeightMapping, ...]:
    """Return a stable plan and fail closed on duplicate or unknown source keys."""

    ordered = sorted(source_keys)
    if len(ordered) != len(set(ordered)):
        raise ValueError("source_keys contains duplicates")
    return tuple(map_core_key(key) for key in ordered)
