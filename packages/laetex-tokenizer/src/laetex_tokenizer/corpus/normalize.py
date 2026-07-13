"""Lossless corpus decoding.

Tokenizer training deliberately applies no Unicode or line-ending normalization:
code points, whitespace, and newline conventions are part of source code.
"""

from __future__ import annotations


class CorpusEncodingError(ValueError):
    """Raised when source bytes are not strict UTF-8."""


def decode_lossless_utf8(data: bytes) -> str:
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise CorpusEncodingError(
            "tokenizer corpus objects must be strict UTF-8; transcode upstream "
            "and record that transformation in lineage"
        ) from error
    if text.encode("utf-8", errors="strict") != data:
        raise CorpusEncodingError("UTF-8 decode/encode round-trip failed")
    return text


def normalize_identity(text: str) -> str:
    """Return text unchanged; the function makes the contract explicit."""
    text.encode("utf-8", errors="strict")
    return text
