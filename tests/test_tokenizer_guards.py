"""Tokenizer contracts: local synthetic only; production remains RunPod-gated."""

from __future__ import annotations

from pathlib import Path

import pytest

from laetex_tokenizer.corpus.sample import LOCAL_TEST_MAX_BYTES, synthetic_documents
from laetex_tokenizer.pipeline import _enforce_execution_boundary


def test_local_synthetic_byte_budget() -> None:
    docs = synthetic_documents()
    total = sum(doc.byte_count for doc in docs)
    assert 0 < total <= LOCAL_TEST_MAX_BYTES


def test_production_mode_requires_runpod(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("RUNPOD_POD_ID", raising=False)
    args = type(
        "Args",
        (),
        {"execution_mode": "runpod", "test_mode": False},
    )()
    with pytest.raises(RuntimeError, match="RunPod-only"):
        _enforce_execution_boundary(args)


def test_test_mode_requires_explicit_flag() -> None:
    args = type(
        "Args",
        (),
        {"execution_mode": "test", "test_mode": False},
    )()
    with pytest.raises(RuntimeError, match="--test-mode"):
        _enforce_execution_boundary(args)


def test_tokenizer_training_contract_files(repo_root: Path) -> None:
    # Contract presence only; full BPE training is RunPod-scoped.
    train_cfg = repo_root / "configs" / "e01" / "tokenizer" / "train-128k.yaml"
    assert train_cfg.is_file()
    text = train_cfg.read_text(encoding="utf-8")
    assert "byte_level_bpe" in text
    assert "vocab_size: 128000" in text
    assert "RUNPOD_POD_ID" in text
