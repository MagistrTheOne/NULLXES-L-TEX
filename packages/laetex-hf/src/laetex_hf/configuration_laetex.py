from __future__ import annotations

from dataclasses import asdict, is_dataclass
from importlib import import_module
from typing import Any, Mapping

from ._imports import require_transformers

require_transformers()

from transformers import PretrainedConfig  # noqa: E402


_CORE_CONFIG_CANDIDATES = (
    ("laetex_core.config", "LaetexConfig"),
    ("laetex_core.config", "LaetexModelConfig"),
    ("laetex_core", "LaetexConfig"),
)

_CORE_FIELDS = (
    "vocab_size",
    "hidden_size",
    "num_hidden_layers",
    "num_attention_heads",
    "num_key_value_heads",
    "head_dim",
    "intermediate_size",
    "moe_intermediate_size",
    "num_experts",
    "num_experts_per_tok",
    "shared_expert_intermediate_size",
    "max_position_embeddings",
    "rms_norm_eps",
    "rope_theta",
    "attention_bias",
    "attention_dropout",
    "qk_norm",
    "router_score_function",
    "tie_word_embeddings",
    "use_cache",
    "initializer_range",
)

_CORE_TO_HF_ALIASES = {
    "layers": "num_hidden_layers",
    "query_heads": "num_attention_heads",
    "key_value_heads": "num_key_value_heads",
    "expert_intermediate_size": "moe_intermediate_size",
    "routed_experts": "num_experts",
    "experts_per_token": "num_experts_per_tok",
}


def _config_dict(config: Any) -> dict[str, Any]:
    if isinstance(config, Mapping):
        return dict(config)
    if is_dataclass(config) and not isinstance(config, type):
        return asdict(config)
    for method_name in ("model_dump", "to_dict"):
        method = getattr(config, method_name, None)
        if callable(method):
            return dict(method())
    if hasattr(config, "__dict__"):
        return {key: value for key, value in vars(config).items() if not key.startswith("_")}
    raise TypeError(f"Cannot convert {type(config).__name__} to a configuration mapping")


def _resolve_core_config_class() -> type[Any]:
    errors: list[str] = []
    for module_name, class_name in _CORE_CONFIG_CANDIDATES:
        try:
            candidate = getattr(import_module(module_name), class_name)
        except (ImportError, AttributeError) as exc:
            errors.append(f"{module_name}.{class_name}: {exc}")
            continue
        if isinstance(candidate, type):
            return candidate
    raise ImportError(
        "No supported laetex-core configuration class was found. Expected one of: "
        + ", ".join(f"{module}.{name}" for module, name in _CORE_CONFIG_CANDIDATES)
        + ". Resolution errors: "
        + "; ".join(errors)
    )


class LaetexConfig(PretrainedConfig):
    """Transformers view of the stable LÆTEX core model contract."""

    model_type = "laetex_moe"
    keys_to_ignore_at_inference = ["past_key_values"]

    def __init__(
        self,
        *,
        vocab_size: int = 151_936,
        hidden_size: int = 6_144,
        num_hidden_layers: int = 62,
        num_attention_heads: int = 96,
        num_key_value_heads: int = 8,
        head_dim: int = 128,
        intermediate_size: int = 0,
        moe_intermediate_size: int = 2_560,
        num_experts: int = 160,
        num_experts_per_tok: int = 8,
        shared_expert_intermediate_size: int = 0,
        max_position_embeddings: int = 262_144,
        rms_norm_eps: float = 1e-6,
        rope_theta: float = 10_000_000.0,
        attention_bias: bool = False,
        attention_dropout: float = 0.0,
        qk_norm: bool = True,
        router_score_function: str = "softmax",
        tie_word_embeddings: bool = False,
        use_cache: bool = True,
        initializer_range: float = 0.02,
        **kwargs: Any,
    ) -> None:
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.num_key_value_heads = num_key_value_heads
        self.head_dim = head_dim
        self.intermediate_size = intermediate_size
        self.moe_intermediate_size = moe_intermediate_size
        self.num_experts = num_experts
        self.num_experts_per_tok = num_experts_per_tok
        self.shared_expert_intermediate_size = shared_expert_intermediate_size
        self.max_position_embeddings = max_position_embeddings
        self.rms_norm_eps = rms_norm_eps
        self.rope_theta = rope_theta
        self.attention_bias = attention_bias
        self.attention_dropout = attention_dropout
        self.qk_norm = qk_norm
        self.router_score_function = router_score_function
        self.use_cache = use_cache
        self.initializer_range = initializer_range
        super().__init__(tie_word_embeddings=tie_word_embeddings, **kwargs)
        self._validate_shape_contract()

    def _validate_shape_contract(self) -> None:
        if self.hidden_size <= 0 or self.num_hidden_layers <= 0:
            raise ValueError("hidden_size and num_hidden_layers must be positive")
        if self.num_attention_heads <= 0 or self.num_key_value_heads <= 0:
            raise ValueError("attention head counts must be positive")
        if self.num_attention_heads % self.num_key_value_heads:
            raise ValueError("num_attention_heads must be divisible by num_key_value_heads")
        if self.num_attention_heads * self.head_dim < self.hidden_size:
            raise ValueError("num_attention_heads * head_dim cannot be smaller than hidden_size")
        if not 0 < self.num_experts_per_tok <= self.num_experts:
            raise ValueError("num_experts_per_tok must be in [1, num_experts]")

    @classmethod
    def from_core_config(cls, core_config: Any, **overrides: Any) -> "LaetexConfig":
        values = {
            _CORE_TO_HF_ALIASES.get(key, key): value
            for key, value in _config_dict(core_config).items()
        }
        values.update(overrides)
        return cls(**values)

    def to_core_dict(self) -> dict[str, Any]:
        return {key: getattr(self, key) for key in _CORE_FIELDS}

    def to_core_config(self, config_class: type[Any] | None = None) -> Any:
        target = config_class or _resolve_core_config_class()
        values = self.to_core_dict()
        try:
            return target(**values)
        except TypeError as exc:
            raise TypeError(
                f"{target.__module__}.{target.__name__} rejected the LÆTEX config fields. "
                "The laetex-core and laetex-hf package versions are incompatible."
            ) from exc
