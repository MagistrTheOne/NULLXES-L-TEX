"""Shared fixtures for CPU-only LÆTEX unit tests.

No GPU, no model training, no weight downloads.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SRC = [
    REPO_ROOT / "packages" / "laetex-validation" / "src",
    REPO_ROOT / "packages" / "laetex-core" / "src",
    REPO_ROOT / "packages" / "laetex-hf" / "src",
    REPO_ROOT / "packages" / "laetex-megatron" / "src",
    REPO_ROOT / "packages" / "laetex-tokenizer" / "src",
]


@pytest.fixture(scope="session", autouse=True)
def _ensure_package_paths() -> None:
    for path in PACKAGE_SRC:
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def schema_path(repo_root: Path) -> Path:
    return repo_root / "schemas" / "laetex-model-config.v1.json"


@pytest.fixture(scope="session")
def tiny_cpu_config_path(repo_root: Path) -> Path:
    return repo_root / "configs" / "e01" / "tiny-cpu.yaml"


@pytest.fixture(scope="session")
def target_config_path(repo_root: Path) -> Path:
    return repo_root / "configs" / "e01" / "latex-e01-480a35.yaml"
