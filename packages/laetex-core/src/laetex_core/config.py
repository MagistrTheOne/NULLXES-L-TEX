from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


def _pick(mapping: Mapping[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in mapping:
            return mapping[name]
    return default


@dataclass(frozen=True)
class AttentionConfig:
    query_heads: int
    key_value_heads: int
    head_dim: int
    qkv_bias: bool = False
    qk_norm: bool = False
    rope_theta: float = 1_000_000.0
    mode: str = "global"
    sliding_window: int | None = None

    def __post_init__(self) -> None:
        if min(self.query_heads, self.key_value_heads, self.head_dim) <= 0:
            raise ValueError("attention dimensions must be positive")
        if self.query_heads % self.key_value_heads:
            raise ValueError("query_heads must be divisible by key_value_heads")
        if self.head_dim % 2:
            raise ValueError("RoPE requires an even head_dim")
        if self.mode not in {"global", "local"}:
            raise ValueError("attention mode must be 'global' or 'local'")
        if self.mode == "local" and (self.sliding_window is None or self.sliding_window <= 0):
            raise ValueError("local attention requires a positive sliding_window")


@dataclass(frozen=True)
class MoEConfig:
    routed_experts: int
    experts_per_token: int
    expert_intermediate_size: int
    shared_experts: int = 1
    router_bias_update_rate: float = 1e-3

    def __post_init__(self) -> None:
        if self.routed_experts <= 0:
            raise ValueError("routed_experts must be positive")
        if not 0 < self.experts_per_token <= self.routed_experts:
            raise ValueError("experts_per_token must be in [1, routed_experts]")
        if self.expert_intermediate_size <= 0:
            raise ValueError("expert_intermediate_size must be positive")
        if self.shared_experts < 0:
            raise ValueError("shared_experts cannot be negative")
        if self.router_bias_update_rate < 0:
            raise ValueError("router_bias_update_rate cannot be negative")


@dataclass(frozen=True)
class LaetexConfig:
    vocab_size: int
    hidden_size: int
    layers: int
    max_position_embeddings: int
    attention: AttentionConfig
    moe: MoEConfig
    rms_norm_eps: float = 1e-6
    tie_word_embeddings: bool = False
    initializer_range: float = 0.02
    attention_modes: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if min(self.vocab_size, self.hidden_size, self.layers, self.max_position_embeddings) <= 0:
            raise ValueError("model dimensions must be positive")
        if self.rms_norm_eps <= 0 or self.initializer_range <= 0:
            raise ValueError("normalization epsilon and initializer range must be positive")
        if self.attention_modes:
            if len(self.attention_modes) != self.layers:
                raise ValueError("attention_modes must contain exactly one mode per layer")
            if any(mode not in {"global", "local"} for mode in self.attention_modes):
                raise ValueError("attention_modes values must be 'global' or 'local'")
            if "local" in self.attention_modes and not self.attention.sliding_window:
                raise ValueError("local layers require attention.sliding_window")

    def attention_mode_for_layer(self, layer_index: int) -> str:
        return self.attention_modes[layer_index] if self.attention_modes else self.attention.mode

    @classmethod
    def from_dict(cls, document: Mapping[str, Any]) -> "LaetexConfig":
        """Load either the canonical Model YAML document or a direct architecture mapping."""
        spec = document.get("spec", document)
        architecture = spec.get("architecture", spec)
        attention_raw = architecture.get("attention", {})
        moe_raw = architecture.get("moe", {})
        attention_pattern = architecture.get("attention_pattern", {})
        position_raw = architecture.get("position", {})
        normalization_raw = architecture.get("normalization", {})
        layers = int(_pick(architecture, "layers", "num_layers", "num_hidden_layers"))
        sliding_window = _optional_int(
            _pick(
                attention_raw,
                "sliding_window",
                default=_pick(attention_pattern, "local_window"),
            )
        )

        attention = AttentionConfig(
            query_heads=int(_pick(attention_raw, "query_heads", "num_attention_heads")),
            key_value_heads=int(_pick(attention_raw, "key_value_heads", "num_key_value_heads")),
            head_dim=int(_pick(attention_raw, "head_dim")),
            qkv_bias=bool(_pick(attention_raw, "qkv_bias", "attention_bias", default=False)),
            qk_norm=bool(_pick(attention_raw, "qk_norm", default=False)),
            rope_theta=float(
                _pick(
                    attention_raw,
                    "rope_theta",
                    default=_pick(position_raw, "rope_theta", default=1_000_000.0),
                )
            ),
            mode=str(_pick(attention_raw, "mode", default="global")),
            sliding_window=sliding_window,
        )
        moe = MoEConfig(
            routed_experts=int(_pick(moe_raw, "routed_experts", "num_experts")),
            experts_per_token=int(_pick(moe_raw, "experts_per_token", "top_k")),
            expert_intermediate_size=int(
                _pick(moe_raw, "expert_intermediate_size", "intermediate_size")
            ),
            shared_experts=int(_pick(moe_raw, "shared_experts", default=1)),
            router_bias_update_rate=float(
                _pick(moe_raw, "router_bias_update_rate", default=1e-3)
            ),
        )
        modes: Sequence[str] = _pick(architecture, "attention_modes", default=())
        if not modes and attention_pattern:
            local_layers = int(_pick(attention_pattern, "local_layers", default=0))
            global_layers = int(_pick(attention_pattern, "global_layers", default=0))
            cycle = ("local",) * local_layers + ("global",) * global_layers
            if not cycle:
                raise ValueError("attention_pattern must define local_layers or global_layers")
            modes = tuple(cycle[index % len(cycle)] for index in range(layers))
        return cls(
            vocab_size=int(_pick(architecture, "vocab_size")),
            hidden_size=int(_pick(architecture, "hidden_size")),
            layers=layers,
            max_position_embeddings=int(
                _pick(
                    architecture,
                    "max_position_embeddings",
                    default=_pick(attention_pattern, "max_context", default=262_144),
                )
            ),
            attention=attention,
            moe=moe,
            rms_norm_eps=float(
                _pick(
                    architecture,
                    "rms_norm_eps",
                    default=_pick(normalization_raw, "epsilon", default=1e-6),
                )
            ),
            tie_word_embeddings=bool(
                _pick(architecture, "tie_word_embeddings", default=False)
            ),
            initializer_range=float(_pick(architecture, "initializer_range", default=0.02)),
            attention_modes=tuple(str(mode) for mode in modes),
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> "LaetexConfig":
        with Path(path).open("r", encoding="utf-8") as handle:
            document = yaml.safe_load(handle)
        if not isinstance(document, Mapping):
            raise ValueError("configuration YAML must contain a mapping")
        return cls.from_dict(document)


def load_config(path: str | Path) -> LaetexConfig:
    return LaetexConfig.from_yaml(path)


def _optional_int(value: Any) -> int | None:
    return None if value is None else int(value)
