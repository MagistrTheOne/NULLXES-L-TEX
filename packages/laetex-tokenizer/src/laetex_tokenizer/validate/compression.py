"""Compression metrics for held-out tokenizer text."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from tokenizers import Tokenizer


def measure_compression(tokenizer: Tokenizer, texts: Iterable[str]) -> dict[str, Any]:
    document_count = 0
    byte_count = 0
    character_count = 0
    token_count = 0
    per_document: list[dict[str, float | int]] = []

    for text in texts:
        tokens = len(tokenizer.encode(text).ids)
        raw_bytes = len(text.encode("utf-8"))
        characters = len(text)
        if tokens == 0 and text:
            raise ValueError("non-empty text encoded to zero tokens")
        document_count += 1
        byte_count += raw_bytes
        character_count += characters
        token_count += tokens
        per_document.append(
            {
                "bytes": raw_bytes,
                "characters": characters,
                "tokens": tokens,
                "bytes_per_token": raw_bytes / max(tokens, 1),
            }
        )

    if document_count == 0 or token_count == 0:
        raise ValueError("compression gate requires non-empty held-out text")
    return {
        "documents": document_count,
        "bytes": byte_count,
        "characters": character_count,
        "tokens": token_count,
        "bytes_per_token": byte_count / token_count,
        "characters_per_token": character_count / token_count,
        "per_document": per_document,
    }
