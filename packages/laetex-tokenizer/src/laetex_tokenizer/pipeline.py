"""End-to-end tokenizer sampling, training, validation, and attestation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from .corpus.sample import (
    LOCAL_TEST_MAX_BYTES,
    deterministic_sample,
    iter_utf8_files,
    split_documents,
    synthetic_documents,
)
from .manifest import load_manifest, manifest_hash, sha256_bytes
from .train.bpe_trainer import save_tokenizer, train_byte_bpe
from .validate.compression import measure_compression
from .validate.specials import validate_roundtrip, validate_special_tokens


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execution-mode", choices=("runpod", "test"), required=True)
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Required for local synthetic execution; forbidden for production training.",
    )
    return parser.parse_args(argv)


def _enforce_execution_boundary(args: argparse.Namespace) -> None:
    if args.execution_mode == "test":
        if not args.test_mode:
            raise RuntimeError("local execution requires explicit --test-mode")
        return
    if args.test_mode:
        raise RuntimeError("--test-mode cannot be combined with RunPod production mode")
    if not os.environ.get("RUNPOD_POD_ID"):
        raise RuntimeError("real tokenizer training is RunPod-only; RUNPOD_POD_ID is absent")


def _load_config(path: Path) -> dict[str, Any]:
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    if config.get("schema") != "laetex.tokenizer.training/v1":
        raise ValueError("unsupported tokenizer training config schema")
    if config["tokenizer"]["type"] != "byte_level_bpe":
        raise ValueError("only byte_level_bpe is supported")
    if config["tokenizer"]["vocab_size"] != 128_000:
        raise ValueError("the custom tokenizer contract requires vocab_size=128000")
    if config["normalization"] != {"unicode": "identity", "line_endings": "preserve"}:
        raise ValueError("config requests destructive normalization")
    return config


def _tree_hash(root: Path) -> str:
    hasher = hashlib.sha256()
    paths = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
    for path in paths:
        relative = path.name if root.is_file() else path.relative_to(root).as_posix()
        hasher.update(relative.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        hasher.update(b"\0")
    return f"sha256:{hasher.hexdigest()}"


def _production_documents(manifest: dict[str, Any]) -> list[Any]:
    documents = []
    for source in manifest["sources"]:
        local_path = source.get("local_path")
        if not local_path:
            raise ValueError(f"{source['source_id']}: local_path is required in RunPod mode")
        root = Path(local_path)
        observed = _tree_hash(root)
        expected = f"sha256:{source['content_hash']['value']}"
        if observed != expected:
            raise ValueError(
                f"{source['source_id']}: source hash mismatch ({observed} != {expected})"
            )
        documents.extend(iter_utf8_files(source["source_id"], root))
    return documents


def _hash_artifacts(output: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(item for item in output.iterdir() if item.is_file()):
        if path.name == "training-attestation.json":
            continue
        result[path.name] = sha256_bytes(path.read_bytes())
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    _enforce_execution_boundary(args)
    config = _load_config(args.config)
    corpus_manifest = load_manifest(args.manifest, args.schema)

    if args.execution_mode == "test":
        if any(source.get("local_path") for source in corpus_manifest["sources"]):
            raise RuntimeError("test mode rejects configured corpus paths")
        documents = synthetic_documents()
        sample_limit = LOCAL_TEST_MAX_BYTES
    else:
        documents = _production_documents(corpus_manifest)
        sample_limit = config["sampling"]["max_bytes"]

    sampled = deterministic_sample(
        documents, seed=config["sampling"]["seed"], max_bytes=sample_limit
    )
    sampled_bytes = sum(document.byte_count for document in sampled)
    if args.execution_mode == "test" and sampled_bytes > LOCAL_TEST_MAX_BYTES:
        raise RuntimeError("local synthetic input exceeded the 1 MiB hard limit")

    train_documents, validation_documents = split_documents(
        sampled,
        validation_fraction=config["sampling"]["validation_fraction"],
        seed=config["sampling"]["seed"],
    )
    tokenizer = train_byte_bpe(
        (document.text for document in train_documents),
        vocab_size=config["tokenizer"]["vocab_size"],
        min_frequency=config["tokenizer"]["min_frequency"],
        special_tokens=corpus_manifest["tokenizer"]["special_tokens"],
        test_mode=args.test_mode,
    )
    realized_vocab = tokenizer.get_vocab_size(with_added_tokens=True)
    if args.execution_mode == "runpod" and realized_vocab != 128_000:
        raise ValueError(f"production vocabulary is {realized_vocab}, expected exactly 128000")

    special_ids = validate_special_tokens(
        tokenizer, corpus_manifest["tokenizer"]["special_tokens"]
    )
    roundtrip_documents = validate_roundtrip(
        tokenizer, (document.text for document in validation_documents)
    )
    compression = measure_compression(
        tokenizer, (document.text for document in validation_documents)
    )

    args.output.mkdir(parents=True, exist_ok=True)
    save_tokenizer(tokenizer, args.output)
    attestation = {
        "schema": "laetex.tokenizer.attestation/v1",
        "created_at": datetime.now(UTC).isoformat(),
        "execution": {
            "mode": args.execution_mode,
            "runpod_pod_id": os.environ.get("RUNPOD_POD_ID"),
            "python": sys.version,
            "platform": platform.platform(),
        },
        "inputs": {
            "config_sha256": sha256_bytes(args.config.read_bytes()),
            "manifest_sha256": manifest_hash(corpus_manifest),
            "sampled_documents": len(sampled),
            "sampled_bytes": sampled_bytes,
            "train_documents": len(train_documents),
            "validation_documents": len(validation_documents),
        },
        "tokenizer": {
            "target_vocab_size": 128_000,
            "realized_vocab_size": realized_vocab,
            "byte_fallback": True,
            "normalization": {"unicode": "identity", "line_endings": "preserve"},
            "special_token_ids": special_ids,
        },
        "validation": {
            "roundtrip_documents": roundtrip_documents,
            "compression": compression,
        },
    }
    attestation["artifact_hashes"] = _hash_artifacts(args.output)
    attestation_path = args.output / "training-attestation.json"
    attestation_path.write_text(
        json.dumps(attestation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return attestation


def main(argv: list[str] | None = None) -> int:
    try:
        result = run(_parse_args(argv))
    except Exception as error:
        print(f"laetex-tokenizer: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
