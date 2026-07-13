"""Repository policy guards: no weight parent, H200-only RunPod profiles."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


CANONICAL_CONFIGS = [
    "configs/e01/tiny-cpu.yaml",
    "configs/e01/proxy-1b.yaml",
    "configs/e01/proxy-7b.yaml",
    "configs/e01/proxy-30b.yaml",
    "configs/e01/latex-e01-480a35.yaml",
    "model/latex-e01-480a35.yaml",
]


@pytest.mark.parametrize("relpath", CANONICAL_CONFIGS)
def test_canonical_configs_have_null_weight_parent(repo_root: Path, relpath: str) -> None:
    path = repo_root / relpath
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert doc["provenance"]["weight_parent"] is None
    assert doc["provenance"]["initialization"] == "independent-random-init"


def test_canonical_stages_are_independent(repo_root: Path) -> None:
    stages = sorted((repo_root / "model" / "stages").glob("*.yaml"))
    assert stages, "expected independent stage manifests"
    forbidden_ids = {
        "S0-UPSTREAM",
        "S1-IDENTITY",
        "M1-IDENTITY-MERGED",
        "S2-ACTION-SFT",
        "M2-ACTION-MERGED",
        "S3-PREFERENCE",
        "M3-PREFERENCE-MERGED",
        "S4-GRPO",
        "M4-RELEASE",
    }
    for path in stages:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        stage_id = doc["metadata"]["id"]
        assert stage_id not in forbidden_ids
        assert doc["metadata"]["status"] in {"planned", "archived", "research-only"}
        assert "Qwen/" not in path.read_text(encoding="utf-8")


def test_runpod_profiles_are_h200_only(repo_root: Path) -> None:
    profiles = list((repo_root / "infra" / "runpod" / "profiles").glob("*.yaml"))
    assert profiles
    for path in profiles:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        platform = doc.get("platform") or {}
        accelerator = str(platform.get("accelerator", "")).upper()
        assert "H200" in accelerator, path.name
        assert platform.get("local_model_workloads") in {False, "forbidden", None} or (
            str(platform.get("local_model_workloads")).lower() == "forbidden"
        )
        text = path.read_text(encoding="utf-8").lower()
        assert "rtx 4090" not in text
        assert "rtx 5090" not in text
        assert "google colab" not in text


def test_readme_declares_independent_e01(repo_root: Path) -> None:
    text = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "ADR-0007" in text
    assert "weight parent" in text.lower() or "weight_parent" in text
    assert "from-scratch" in text.lower() or "from scratch" in text.lower()
