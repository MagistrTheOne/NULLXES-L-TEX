"""CPU-reference forward shapes for the tiny proxy only."""

from __future__ import annotations

from pathlib import Path

import pytest
import torch

from laetex_core import LaetexConfig, LaetexForCausalLM


@pytest.fixture
def tiny_config(tiny_cpu_config_path: Path) -> LaetexConfig:
    return LaetexConfig.from_yaml(tiny_cpu_config_path)


def test_refuses_full_target_materialization(target_config_path: Path) -> None:
    config = LaetexConfig.from_yaml(target_config_path)
    with pytest.raises(ValueError, match="refusing to materialize"):
        LaetexForCausalLM(config)


def test_tiny_forward_logits_shape(tiny_config: LaetexConfig) -> None:
    model = LaetexForCausalLM(tiny_config)
    model.eval()
    batch, seq = 2, 8
    input_ids = torch.randint(0, tiny_config.vocab_size, (batch, seq))
    with torch.no_grad():
        out = model(input_ids)
    assert out.logits.shape == (batch, seq, tiny_config.vocab_size)
    assert out.loss is None
    assert len(out.router_outputs) == tiny_config.layers


def test_tiny_causal_loss(tiny_config: LaetexConfig) -> None:
    model = LaetexForCausalLM(tiny_config)
    model.train()
    input_ids = torch.randint(0, tiny_config.vocab_size, (1, 6))
    out = model(input_ids, labels=input_ids)
    assert out.loss is not None
    assert torch.isfinite(out.loss)
    out.loss.backward()


def test_hybrid_attention_modes(tiny_config: LaetexConfig) -> None:
    assert len(tiny_config.attention_modes) == tiny_config.layers
    assert "local" in tiny_config.attention_modes
    assert "global" in tiny_config.attention_modes
    # 3 local + 1 global cycle for 8 layers
    assert tiny_config.attention_modes == (
        "local",
        "local",
        "local",
        "global",
        "local",
        "local",
        "local",
        "global",
    )


def test_kv_cache_extends_sequence(tiny_config: LaetexConfig) -> None:
    model = LaetexForCausalLM(tiny_config)
    model.eval()
    first = torch.randint(0, tiny_config.vocab_size, (1, 4))
    with torch.no_grad():
        step1 = model(first, use_cache=True)
        assert step1.past_key_values is not None
        second = torch.randint(0, tiny_config.vocab_size, (1, 1))
        step2 = model(second, past_key_values=step1.past_key_values, use_cache=True)
    assert step2.logits.shape == (1, 1, tiny_config.vocab_size)
    assert step2.past_key_values is not None
    assert step2.past_key_values[0][0].shape[-2] == 5
