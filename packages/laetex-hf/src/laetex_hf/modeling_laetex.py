from __future__ import annotations

from importlib import import_module
from typing import Any

from ._imports import require_transformers
from .configuration_laetex import LaetexConfig

require_transformers()

from transformers import PreTrainedModel  # noqa: E402


_CORE_MODEL_CANDIDATES = (
    ("laetex_core.modeling", "LaetexForCausalLM"),
    ("laetex_core.model", "LaetexForCausalLM"),
    ("laetex_core", "LaetexForCausalLM"),
)


def _build_core_model(config: LaetexConfig) -> Any:
    errors: list[str] = []
    for module_name, class_name in _CORE_MODEL_CANDIDATES:
        try:
            model_class = getattr(import_module(module_name), class_name)
        except (ImportError, AttributeError) as exc:
            errors.append(f"{module_name}.{class_name}: {exc}")
            continue
        try:
            return model_class(config.to_core_config())
        except Exception as exc:
            raise RuntimeError(
                f"Failed to construct {module_name}.{class_name} from LaetexConfig"
            ) from exc
    raise ImportError(
        "No supported laetex-core causal LM implementation was found. Expected one of: "
        + ", ".join(f"{module}.{name}" for module, name in _CORE_MODEL_CANDIDATES)
        + ". Resolution errors: "
        + "; ".join(errors)
    )


class LaetexForCausalLM(PreTrainedModel):
    """Thin Transformers lifecycle wrapper around the authoritative core model."""

    config_class = LaetexConfig
    base_model_prefix = "core_model"
    main_input_name = "input_ids"
    _supports_cache_class = True
    _supports_sdpa = True

    def __init__(self, config: LaetexConfig, core_model: Any | None = None) -> None:
        super().__init__(config)
        self.core_model = core_model if core_model is not None else _build_core_model(config)

    def forward(
        self,
        input_ids: Any = None,
        attention_mask: Any = None,
        position_ids: Any = None,
        past_key_values: Any = None,
        inputs_embeds: Any = None,
        labels: Any = None,
        use_cache: bool | None = None,
        output_attentions: bool | None = None,
        output_hidden_states: bool | None = None,
        return_dict: bool | None = None,
        cache_position: Any = None,
        **kwargs: Any,
    ) -> Any:
        return self.core_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            labels=labels,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            cache_position=cache_position,
            **kwargs,
        )

    def get_input_embeddings(self) -> Any:
        getter = getattr(self.core_model, "get_input_embeddings", None)
        if not callable(getter):
            raise AttributeError("laetex-core model does not expose get_input_embeddings()")
        return getter()

    def set_input_embeddings(self, value: Any) -> None:
        setter = getattr(self.core_model, "set_input_embeddings", None)
        if not callable(setter):
            raise AttributeError("laetex-core model does not expose set_input_embeddings()")
        setter(value)

    def get_output_embeddings(self) -> Any:
        getter = getattr(self.core_model, "get_output_embeddings", None)
        return getter() if callable(getter) else None

    def set_output_embeddings(self, value: Any) -> None:
        setter = getattr(self.core_model, "set_output_embeddings", None)
        if not callable(setter):
            raise AttributeError("laetex-core model does not expose set_output_embeddings()")
        setter(value)

    def prepare_inputs_for_generation(self, input_ids: Any, **kwargs: Any) -> dict[str, Any]:
        prepare = getattr(self.core_model, "prepare_inputs_for_generation", None)
        if callable(prepare):
            return prepare(input_ids, **kwargs)
        return {"input_ids": input_ids, **kwargs}

    def _reorder_cache(self, past_key_values: Any, beam_idx: Any) -> Any:
        reorder = getattr(self.core_model, "_reorder_cache", None)
        if not callable(reorder):
            raise NotImplementedError("laetex-core model does not support beam-cache reordering")
        return reorder(past_key_values, beam_idx)
