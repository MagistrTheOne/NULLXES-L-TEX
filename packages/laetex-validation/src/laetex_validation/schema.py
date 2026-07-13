"""JSON Schema loading and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

SCHEMA_FILENAME = "laetex-model-config.v1.json"


def find_schema(start: Path | None = None) -> Path:
    """Find the repository schema without assuming the package is installed."""
    candidates = [Path.cwd(), *(start or Path(__file__).resolve()).parents]
    for directory in candidates:
        candidate = directory / "schemas" / SCHEMA_FILENAME
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Could not locate schemas/{SCHEMA_FILENAME}")


def load_schema(path: str | Path | None = None) -> dict[str, Any]:
    schema_path = Path(path) if path is not None else find_schema()
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(
    config: Mapping[str, Any], schema_path: str | Path | None = None
) -> None:
    validator = Draft202012Validator(load_schema(schema_path))
    errors = sorted(validator.iter_errors(config), key=lambda error: list(error.path))
    if errors:
        messages = []
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            messages.append(f"{location}: {error.message}")
        raise ValueError("Schema validation failed:\n" + "\n".join(messages))
