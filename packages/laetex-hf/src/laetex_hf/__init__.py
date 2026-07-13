from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._imports import (
    TRANSFORMERS_AVAILABLE,
    MissingTransformersError,
    require_transformers,
)
from .auto import register_with_transformers

if TYPE_CHECKING:
    from .configuration_laetex import LaetexConfig
    from .modeling_laetex import LaetexForCausalLM

__all__ = [
    "LaetexConfig",
    "LaetexForCausalLM",
    "MissingTransformersError",
    "TRANSFORMERS_AVAILABLE",
    "register_with_transformers",
    "require_transformers",
]


def __getattr__(name: str) -> Any:
    if name == "LaetexConfig":
        require_transformers()
        from .configuration_laetex import LaetexConfig

        return LaetexConfig
    if name == "LaetexForCausalLM":
        require_transformers()
        from .modeling_laetex import LaetexForCausalLM

        return LaetexForCausalLM
    raise AttributeError(name)
