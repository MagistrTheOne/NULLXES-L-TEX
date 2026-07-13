"""Special-token and lossless round-trip gates."""

from __future__ import annotations

from typing import Iterable

from tokenizers import Tokenizer


def validate_special_tokens(tokenizer: Tokenizer, expected: list[str]) -> dict[str, int]:
    vocabulary = tokenizer.get_vocab()
    ids: dict[str, int] = {}
    for token in expected:
        if token not in vocabulary:
            raise ValueError(f"missing special token: {token}")
        encoded = tokenizer.encode(token)
        token_id = vocabulary[token]
        if encoded.ids != [token_id]:
            raise ValueError(f"special token does not encode atomically: {token}")
        ids[token] = token_id
    if len(set(ids.values())) != len(ids):
        raise ValueError("special token IDs are not unique")
    return ids


def validate_roundtrip(tokenizer: Tokenizer, texts: Iterable[str]) -> int:
    checked = 0
    for text in texts:
        decoded = tokenizer.decode(tokenizer.encode(text).ids, skip_special_tokens=False)
        if decoded != text:
            raise ValueError(
                f"lossless round-trip failed at document {checked}: "
                f"expected {text[:80]!r}, got {decoded[:80]!r}"
            )
        checked += 1
    if checked == 0:
        raise ValueError("round-trip gate received no documents")
    return checked
