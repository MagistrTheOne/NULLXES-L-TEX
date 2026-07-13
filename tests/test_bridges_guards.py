"""Import-guarded HF and Megatron bridges must not require heavy runtimes."""

from __future__ import annotations

import pytest

from laetex_hf._imports import TRANSFORMERS_AVAILABLE, require_transformers
from laetex_megatron._imports import STUB_MODE, require_megatron_runtime
from laetex_megatron.topology import ParallelTopology, validate_topology


def test_hf_import_guard_without_transformers() -> None:
    if TRANSFORMERS_AVAILABLE:
        pytest.skip("transformers is installed in this environment")
    with pytest.raises(ImportError, match="laetex-hf"):
        require_transformers()


def test_megatron_stub_mode_without_cluster_stack() -> None:
    # Local/CI never ships megatron-core + TE; contracts must remain usable.
    assert STUB_MODE is True or STUB_MODE is False  # bool contract
    if STUB_MODE:
        with pytest.raises(ImportError, match="Megatron runtime"):
            require_megatron_runtime()


def test_topology_math_tp_pp_ep() -> None:
    # Independent EP inside DP: world = TP * PP * CP * DP; EP divides DP.
    result = validate_topology(
        ParallelTopology(
            world_size=1024,
            tensor_parallel=8,
            pipeline_parallel=8,
            expert_parallel=16,
            context_parallel=1,
            num_experts=144,
            num_layers=64,
        )
    )
    assert result.data_parallel == 16
    assert result.expert_data_parallel == 1


def test_topology_rejects_nondivisible_ep() -> None:
    with pytest.raises(ValueError, match="expert_parallel"):
        validate_topology(
            ParallelTopology(
                world_size=512,
                tensor_parallel=8,
                pipeline_parallel=8,
                expert_parallel=16,
                context_parallel=1,
            )
        )
