"""CPU-only validation utilities for LÆTEX model configurations."""

from pathlib import Path
from typing import Any

from .param_count import ParameterCount, count_parameters

__all__ = ["ParameterCount", "count_parameters", "load_and_validate", "load_config"]


def load_config(path: str | Path) -> dict[str, Any]:
    from .config import load_config as _load_config

    return _load_config(path)


def load_and_validate(
    path: str | Path, schema_path: str | Path | None = None
) -> tuple[dict[str, Any], ParameterCount]:
    from .config import load_and_validate as _load_and_validate

    return _load_and_validate(path, schema_path)
