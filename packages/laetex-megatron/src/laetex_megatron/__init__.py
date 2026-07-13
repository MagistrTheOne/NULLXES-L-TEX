from ._imports import (
    MEGATRON_CORE_AVAILABLE,
    STUB_MODE,
    TRANSFORMER_ENGINE_AVAILABLE,
    MissingMegatronRuntimeError,
    require_megatron_runtime,
)
from .config_bridge import MegatronModelArgs, TargetModelConfig, to_megatron_args
from .specs import (
    HybridAttention,
    ModuleSpecPlaceholder,
    SharedExpert,
    SigmoidTopKRouter,
    hybrid_attention_spec,
    materialize_module_spec,
    shared_expert_spec,
    sigmoid_router_spec,
)
from .topology import ParallelTopology, TopologyValidation, validate_topology
from .weight_mapping import (
    MAPPING_CONTRACT_VERSION,
    WeightMapping,
    WeightTransform,
    map_core_key,
    plan_weight_mapping,
)

__all__ = [
    "HybridAttention",
    "MAPPING_CONTRACT_VERSION",
    "MEGATRON_CORE_AVAILABLE",
    "MegatronModelArgs",
    "MissingMegatronRuntimeError",
    "ModuleSpecPlaceholder",
    "ParallelTopology",
    "STUB_MODE",
    "SharedExpert",
    "SigmoidTopKRouter",
    "TRANSFORMER_ENGINE_AVAILABLE",
    "TargetModelConfig",
    "TopologyValidation",
    "WeightMapping",
    "WeightTransform",
    "hybrid_attention_spec",
    "map_core_key",
    "materialize_module_spec",
    "plan_weight_mapping",
    "require_megatron_runtime",
    "shared_expert_spec",
    "sigmoid_router_spec",
    "to_megatron_args",
    "validate_topology",
]
