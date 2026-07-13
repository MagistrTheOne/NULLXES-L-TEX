"""YAML configuration loading and CPU-only validation CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from .invariants import validate_invariants
from .param_count import ParameterCount, count_parameters
from .schema import validate_schema


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ValueError(f"{config_path} must contain a YAML mapping")
    return config


def load_and_validate(
    path: str | Path, schema_path: str | Path | None = None
) -> tuple[dict[str, Any], ParameterCount]:
    config = load_config(path)
    validate_schema(config, schema_path)
    validate_invariants(config)
    return config, count_parameters(config)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate LÆTEX YAML configs and print closed-form parameter counts."
    )
    parser.add_argument("configs", nargs="+", type=Path)
    parser.add_argument("--schema", type=Path)
    args = parser.parse_args()

    results: dict[str, Any] = {}
    for path in args.configs:
        config, counts = load_and_validate(path, args.schema)
        results[str(path)] = {
            "id": config["metadata"]["id"],
            **counts.as_dict(),
        }
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
