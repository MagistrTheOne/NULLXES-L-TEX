"""Manifest loading, policy gates, and reproducible hashing."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class ManifestError(ValueError):
    """Raised when a corpus manifest violates the tokenizer contract."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def load_manifest(path: Path, schema_path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=str)
    if errors:
        details = "; ".join(error.message for error in errors[:8])
        raise ManifestError(f"manifest schema validation failed: {details}")
    enforce_training_policy(manifest)
    return manifest


def enforce_training_policy(manifest: dict[str, Any]) -> None:
    if not manifest["training_allowed"]:
        raise ManifestError("training_allowed must be true")
    if manifest["normalization"]["unicode"] != "identity":
        raise ManifestError("destructive Unicode normalization is forbidden")
    if manifest["normalization"]["line_endings"] != "preserve":
        raise ManifestError("line endings must be preserved")

    expected_specials = manifest["tokenizer"]["special_tokens"]
    if len(expected_specials) != len(set(expected_specials)):
        raise ManifestError("special tokens must be unique")

    for source in manifest["sources"]:
        source_id = source["source_id"]
        if source["license"]["status"] != "approved":
            raise ManifestError(f"{source_id}: license is not approved")
        if source["pii"]["status"] not in {"clear", "sanitized"}:
            raise ManifestError(f"{source_id}: PII status is not train-safe")
        if source["secrets"]["status"] not in {"clear", "sanitized"}:
            raise ManifestError(f"{source_id}: secrets status is not train-safe")
        if source["dedup"]["status"] != "complete":
            raise ManifestError(f"{source_id}: dedup is incomplete")
        if source["content_hash"]["algorithm"] != "sha256":
            raise ManifestError(f"{source_id}: only sha256 source hashes are accepted")


def manifest_hash(manifest: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json(manifest))
