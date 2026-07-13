from __future__ import annotations

from ._imports import require_transformers


def register_with_transformers(*, exist_ok: bool = True) -> None:
    """Register LÆTEX classes with Transformers Auto APIs.

    Registration is explicit to avoid process-wide import side effects.
    """

    require_transformers()
    from transformers import AutoConfig, AutoModelForCausalLM

    from .configuration_laetex import LaetexConfig
    from .modeling_laetex import LaetexForCausalLM

    try:
        AutoConfig.register(LaetexConfig.model_type, LaetexConfig, exist_ok=exist_ok)
        AutoModelForCausalLM.register(LaetexConfig, LaetexForCausalLM, exist_ok=exist_ok)
    except TypeError:
        # Transformers versions predating `exist_ok` still support registration.
        try:
            AutoConfig.register(LaetexConfig.model_type, LaetexConfig)
            AutoModelForCausalLM.register(LaetexConfig, LaetexForCausalLM)
        except ValueError:
            if not exist_ok:
                raise
