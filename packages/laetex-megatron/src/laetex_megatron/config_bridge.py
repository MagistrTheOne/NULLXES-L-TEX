from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class TargetModelConfig:
    """Runtime-neutral model shape consumed by the Megatron bridge."""

    vocab_size: int = 151_936
    hidden_size: int = 6_144
    num_layers: int = 62
    num_attention_heads: int = 96
    num_query_groups: int = 8
    kv_channels: int = 128
    max_position_embeddings: int = 262_144
    num_moe_experts: int = 160
    moe_router_topk: int = 8
    moe_ffn_hidden_size: int = 2_560
    shared_expert_intermediate_size: int = 0
    moe_router_score_function: str = "softmax"
    normalization: str = "RMSNorm"
    norm_epsilon: float = 1e-6
    rotary_base: float = 10_000_000.0
    qk_layernorm: bool = True
    add_bias_linear: bool = False
    untie_embeddings_and_output_weights: bool = True
    hybrid_attention_pattern: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        positive = (
            "vocab_size",
            "hidden_size",
            "num_layers",
            "num_attention_heads",
            "num_query_groups",
            "kv_channels",
            "max_position_embeddings",
            "num_moe_experts",
            "moe_router_topk",
            "moe_ffn_hidden_size",
        )
        for name in positive:
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        if self.num_attention_heads % self.num_query_groups:
            raise ValueError("num_attention_heads must be divisible by num_query_groups")
        if self.moe_router_topk > self.num_moe_experts:
            raise ValueError("moe_router_topk cannot exceed num_moe_experts")
        if self.shared_expert_intermediate_size < 0:
            raise ValueError("shared_expert_intermediate_size cannot be negative")
        if self.moe_router_score_function not in {"softmax", "sigmoid"}:
            raise ValueError("moe_router_score_function must be softmax or sigmoid")
        if self.hybrid_attention_pattern and len(self.hybrid_attention_pattern) != self.num_layers:
            raise ValueError("hybrid_attention_pattern must contain one entry per layer")

    @classmethod
    def from_config(cls, source: Any) -> "TargetModelConfig":
        if isinstance(source, Mapping):
            values = dict(source)
        elif is_dataclass(source) and not isinstance(source, type):
            values = asdict(source)
        elif callable(getattr(source, "model_dump", None)):
            values = dict(source.model_dump())
        elif callable(getattr(source, "to_dict", None)):
            values = dict(source.to_dict())
        else:
            values = vars(source)

        aliases = {
            "num_hidden_layers": "num_layers",
            "num_key_value_heads": "num_query_groups",
            "head_dim": "kv_channels",
            "num_experts": "num_moe_experts",
            "num_experts_per_tok": "moe_router_topk",
            "moe_intermediate_size": "moe_ffn_hidden_size",
            "rms_norm_eps": "norm_epsilon",
            "rope_theta": "rotary_base",
            "qk_norm": "qk_layernorm",
            "attention_bias": "add_bias_linear",
        }
        normalized = {aliases.get(key, key): value for key, value in values.items()}
        accepted = {field.name for field in fields(cls)}
        return cls(**{key: value for key, value in normalized.items() if key in accepted})


@dataclass(frozen=True)
class MegatronModelArgs:
    num_layers: int
    hidden_size: int
    num_attention_heads: int
    num_query_groups: int
    kv_channels: int
    ffn_hidden_size: int
    num_moe_experts: int
    moe_router_topk: int
    moe_ffn_hidden_size: int
    moe_shared_expert_intermediate_size: int
    moe_router_score_function: str
    max_position_embeddings: int
    rotary_base: float
    normalization: str
    layernorm_epsilon: float
    qk_layernorm: bool
    add_bias_linear: bool
    gated_linear_unit: bool
    group_query_attention: bool
    position_embedding_type: str
    untie_embeddings_and_output_weights: bool
    padded_vocab_size: int
    hybrid_attention_pattern: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def to_megatron_args(config: TargetModelConfig | Any) -> MegatronModelArgs:
    target = config if isinstance(config, TargetModelConfig) else TargetModelConfig.from_config(config)
    return MegatronModelArgs(
        num_layers=target.num_layers,
        hidden_size=target.hidden_size,
        num_attention_heads=target.num_attention_heads,
        num_query_groups=target.num_query_groups,
        kv_channels=target.kv_channels,
        ffn_hidden_size=target.moe_ffn_hidden_size,
        num_moe_experts=target.num_moe_experts,
        moe_router_topk=target.moe_router_topk,
        moe_ffn_hidden_size=target.moe_ffn_hidden_size,
        moe_shared_expert_intermediate_size=target.shared_expert_intermediate_size,
        moe_router_score_function=target.moe_router_score_function,
        max_position_embeddings=target.max_position_embeddings,
        rotary_base=target.rotary_base,
        normalization=target.normalization,
        layernorm_epsilon=target.norm_epsilon,
        qk_layernorm=target.qk_layernorm,
        add_bias_linear=target.add_bias_linear,
        gated_linear_unit=True,
        group_query_attention=target.num_query_groups != target.num_attention_heads,
        position_embedding_type="rope",
        untie_embeddings_and_output_weights=target.untie_embeddings_and_output_weights,
        padded_vocab_size=target.vocab_size,
        hybrid_attention_pattern=target.hybrid_attention_pattern,
    )
