from __future__ import annotations

from importlib.util import find_spec


def _available(module: str) -> bool:
    try:
        return find_spec(module) is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        return False


MEGATRON_CORE_AVAILABLE = _available("megatron.core")
TRANSFORMER_ENGINE_AVAILABLE = _available("transformer_engine")
STUB_MODE = not (MEGATRON_CORE_AVAILABLE and TRANSFORMER_ENGINE_AVAILABLE)


class MissingMegatronRuntimeError(ImportError):
    """Raised when runtime materialization is attempted in contract-only mode."""


def require_megatron_runtime() -> None:
    missing = []
    if not MEGATRON_CORE_AVAILABLE:
        missing.append("megatron-core")
    if not TRANSFORMER_ENGINE_AVAILABLE:
        missing.append("transformer-engine[pytorch]")
    if missing:
        raise MissingMegatronRuntimeError(
            "Megatron runtime materialization is unavailable; missing "
            + ", ".join(missing)
            + ". Install `laetex-megatron[megatron]` only in the approved H200 environment. "
            "Pure config, topology, and weight-mapping contracts remain usable in STUB_MODE."
        )
