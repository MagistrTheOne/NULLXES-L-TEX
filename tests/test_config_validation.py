"""Schema, invariants, and closed-form parameter accounting."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from laetex_validation import count_parameters, load_and_validate


CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs" / "e01"


@pytest.mark.parametrize(
    "config_name",
    [
        "tiny-cpu.yaml",
        "proxy-1b.yaml",
        "proxy-7b.yaml",
        "proxy-30b.yaml",
        "latex-e01-480a35.yaml",
    ],
)
def test_all_presets_validate(config_name: str, schema_path: Path) -> None:
    config, counts = load_and_validate(CONFIG_DIR / config_name, schema_path)
    assert config["provenance"]["weight_parent"] is None
    assert config["provenance"]["initialization"] == "independent-random-init"
    assert counts.total > 0
    assert counts.active > 0
    assert counts.active <= counts.total


def test_target_parameter_band(target_config_path: Path, schema_path: Path) -> None:
    """ENGINEERING HYPOTHESIS band: ~480B total / ~35B active."""
    _, counts = load_and_validate(target_config_path, schema_path)
    assert 450_000_000_000 <= counts.total <= 510_000_000_000
    assert 30_000_000_000 <= counts.active <= 40_000_000_000


def test_tiny_cpu_is_materializable(tiny_cpu_config_path: Path, schema_path: Path) -> None:
    _, counts = load_and_validate(tiny_cpu_config_path, schema_path)
    assert counts.total < 100_000_000


def test_qk_norm_changes_count(target_config_path: Path) -> None:
    with target_config_path.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    with_qk = count_parameters(config)
    config["architecture"]["attention"]["qk_norm"] = False
    without_qk = count_parameters(config)
    assert with_qk.total > without_qk.total
