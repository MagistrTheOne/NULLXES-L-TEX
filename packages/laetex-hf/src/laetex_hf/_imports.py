from __future__ import annotations

from importlib.util import find_spec


TRANSFORMERS_AVAILABLE = find_spec("transformers") is not None


class MissingTransformersError(ImportError):
    """Raised when an optional Transformers API is used without Transformers."""


def require_transformers() -> None:
    if not TRANSFORMERS_AVAILABLE:
        raise MissingTransformersError(
            "laetex-hf requires its optional Transformers integration for this API. "
            "Install it with `pip install 'laetex-hf[transformers]'`."
        )
