from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from ._imports import require_megatron_runtime


@runtime_checkable
class HybridAttention(Protocol):
    """Interface required from a custom full/local/linear attention module."""

    def forward(
        self,
        hidden_states: Any,
        attention_mask: Any = None,
        inference_context: Any = None,
        **kwargs: Any,
    ) -> Any: ...


@runtime_checkable
class SigmoidTopKRouter(Protocol):
    """Interface required from a sigmoid-scored, load-balanced MoE router."""

    def route(self, hidden_states: Any) -> tuple[Any, Any]: ...


@runtime_checkable
class SharedExpert(Protocol):
    """Interface required from an always-active shared expert."""

    def forward(self, hidden_states: Any) -> Any: ...


@dataclass(frozen=True)
class ModuleSpecPlaceholder:
    """Serializable contract that can be inspected without Megatron or CUDA."""

    kind: str
    interface: str
    params: dict[str, Any]
    implementation_required: bool = True


def hybrid_attention_spec(
    *,
    layer_pattern: tuple[str, ...],
    full_attention_token: str = "full",
) -> ModuleSpecPlaceholder:
    if not layer_pattern:
        raise ValueError("layer_pattern cannot be empty")
    accepted = {full_attention_token, "local", "linear"}
    unknown = sorted(set(layer_pattern) - accepted)
    if unknown:
        raise ValueError(f"unsupported hybrid attention layer kinds: {unknown}")
    return ModuleSpecPlaceholder(
        kind="hybrid_attention",
        interface=f"{HybridAttention.__module__}.{HybridAttention.__name__}",
        params={
            "layer_pattern": layer_pattern,
            "full_attention_token": full_attention_token,
        },
    )


def sigmoid_router_spec(*, num_experts: int, top_k: int) -> ModuleSpecPlaceholder:
    if num_experts <= 0 or not 0 < top_k <= num_experts:
        raise ValueError("require num_experts > 0 and 0 < top_k <= num_experts")
    return ModuleSpecPlaceholder(
        kind="sigmoid_topk_router",
        interface=f"{SigmoidTopKRouter.__module__}.{SigmoidTopKRouter.__name__}",
        params={"num_experts": num_experts, "top_k": top_k, "score_function": "sigmoid"},
    )


def shared_expert_spec(
    *, hidden_size: int, intermediate_size: int
) -> ModuleSpecPlaceholder:
    if hidden_size <= 0 or intermediate_size <= 0:
        raise ValueError("hidden_size and intermediate_size must be positive")
    return ModuleSpecPlaceholder(
        kind="shared_expert",
        interface=f"{SharedExpert.__module__}.{SharedExpert.__name__}",
        params={"hidden_size": hidden_size, "intermediate_size": intermediate_size},
    )


def materialize_module_spec(
    placeholder: ModuleSpecPlaceholder,
    implementation: type[Any],
) -> Any:
    """Create a Megatron ModuleSpec; caller supplies the audited implementation."""

    require_megatron_runtime()
    from megatron.core.transformer.spec_utils import ModuleSpec

    if not isinstance(implementation, type):
        raise TypeError("implementation must be a module class")
    return ModuleSpec(module=implementation, params=dict(placeholder.params))
