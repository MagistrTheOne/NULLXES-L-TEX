"""Deterministic, exact-hash-deduplicated corpus sampling."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

from .normalize import decode_lossless_utf8, normalize_identity

LOCAL_TEST_MAX_BYTES = 1_048_576


@dataclass(frozen=True)
class Document:
    source_id: str
    object_id: str
    text: str
    byte_count: int
    sha256: str


def iter_utf8_files(source_id: str, root: Path) -> Iterator[Document]:
    if not root.exists():
        raise FileNotFoundError(root)
    paths = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
    for path in paths:
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        yield Document(
            source_id=source_id,
            object_id=path.relative_to(root).as_posix() if root.is_dir() else path.name,
            text=normalize_identity(decode_lossless_utf8(data)),
            byte_count=len(data),
            sha256=digest,
        )


def deterministic_sample(
    documents: Iterable[Document], *, seed: int, max_bytes: int
) -> list[Document]:
    unique: dict[str, Document] = {}
    for document in documents:
        unique.setdefault(document.sha256, document)

    def rank(document: Document) -> bytes:
        value = f"{seed}\0{document.source_id}\0{document.object_id}\0{document.sha256}"
        return hashlib.sha256(value.encode("utf-8")).digest()

    selected: list[Document] = []
    used = 0
    for document in sorted(unique.values(), key=rank):
        if document.byte_count > max_bytes - used:
            continue
        selected.append(document)
        used += document.byte_count
    return selected


def split_documents(
    documents: Iterable[Document], *, validation_fraction: float, seed: int
) -> tuple[list[Document], list[Document]]:
    train: list[Document] = []
    validation: list[Document] = []
    threshold = int(validation_fraction * 10_000)
    for document in documents:
        key = f"{seed}\0split\0{document.sha256}".encode("utf-8")
        bucket = int.from_bytes(hashlib.sha256(key).digest()[:4], "big") % 10_000
        (validation if bucket < threshold else train).append(document)
    if not validation and len(train) > 1:
        validation.append(train.pop())
    if not train:
        raise ValueError("sampling produced no training documents")
    return train, validation


def synthetic_documents() -> list[Document]:
    """Generate a small multilingual/code fixture; never use it for quality claims."""
    snippets = [
        "def verify(value: bytes) -> bool:\n    return value.startswith(b'LÆTEX')\n",
        '{"role":"tool","action":"read","path":"src/app.py"}\n',
        "SELECT asset_id, version FROM state WHERE policy = 'allow';\r\n",
        "fn main() { println!(\"evidence: Δ, 東京, مرحبا\"); }\n",
        "diff --git a/a.py b/a.py\n-unsafe()\n+verified()\n",
    ]
    documents: list[Document] = []
    for index, text in enumerate(snippets):
        data = text.encode("utf-8")
        documents.append(
            Document(
                source_id="synthetic-local-test",
                object_id=f"fixture-{index}",
                text=text,
                byte_count=len(data),
                sha256=hashlib.sha256(data).hexdigest(),
            )
        )
    if sum(document.byte_count for document in documents) > LOCAL_TEST_MAX_BYTES:
        raise AssertionError("synthetic fixture exceeds local test limit")
    return documents
