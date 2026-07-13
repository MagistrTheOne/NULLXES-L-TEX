from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParallelTopology:
    world_size: int
    tensor_parallel: int = 1
    pipeline_parallel: int = 1
    expert_parallel: int = 1
    context_parallel: int = 1
    data_parallel: int | None = None
    num_layers: int | None = None
    num_experts: int | None = None


@dataclass(frozen=True)
class TopologyValidation:
    world_size: int
    tensor_parallel: int
    pipeline_parallel: int
    expert_parallel: int
    context_parallel: int
    data_parallel: int
    model_parallel_product: int
    expert_data_parallel: int


def validate_topology(topology: ParallelTopology) -> TopologyValidation:
    """Validate integer topology only; never imports torch or initializes CUDA."""

    dimensions = {
        "world_size": topology.world_size,
        "tensor_parallel": topology.tensor_parallel,
        "pipeline_parallel": topology.pipeline_parallel,
        "expert_parallel": topology.expert_parallel,
        "context_parallel": topology.context_parallel,
    }
    for name, value in dimensions.items():
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")

    model_parallel = (
        topology.tensor_parallel * topology.pipeline_parallel * topology.context_parallel
    )
    if topology.world_size % model_parallel:
        raise ValueError(
            "world_size must be divisible by TP * PP * CP; EP is formed inside the "
            "resulting data-parallel dimension and is not multiplied twice"
        )
    derived_dp = topology.world_size // model_parallel
    if topology.data_parallel is not None and topology.data_parallel != derived_dp:
        raise ValueError(
            f"data_parallel={topology.data_parallel} does not match derived DP={derived_dp}"
        )
    if derived_dp % topology.expert_parallel:
        raise ValueError("expert_parallel must divide the derived data_parallel dimension")
    if topology.num_experts is not None:
        if topology.num_experts <= 0:
            raise ValueError("num_experts must be positive")
        if topology.num_experts % topology.expert_parallel:
            raise ValueError("num_experts must be divisible by expert_parallel")
    if topology.num_layers is not None:
        if topology.num_layers <= 0:
            raise ValueError("num_layers must be positive")
        if topology.num_layers % topology.pipeline_parallel:
            raise ValueError(
                "num_layers must be divisible by pipeline_parallel in this bridge; "
                "uneven and standalone embedding/loss stages require an explicit schedule"
            )

    return TopologyValidation(
        world_size=topology.world_size,
        tensor_parallel=topology.tensor_parallel,
        pipeline_parallel=topology.pipeline_parallel,
        expert_parallel=topology.expert_parallel,
        context_parallel=topology.context_parallel,
        data_parallel=derived_dp,
        model_parallel_product=model_parallel,
        expert_data_parallel=derived_dp // topology.expert_parallel,
    )
