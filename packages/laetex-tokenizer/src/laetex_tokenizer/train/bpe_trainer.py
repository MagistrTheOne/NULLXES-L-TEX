"""Byte-level BPE construction and artifact export."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers


def train_byte_bpe(
    texts: Iterable[str],
    *,
    vocab_size: int,
    min_frequency: int,
    special_tokens: list[str],
    test_mode: bool,
) -> Tokenizer:
    tokenizer = Tokenizer(models.BPE(byte_fallback=True))
    tokenizer.normalizer = None
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=True)
    tokenizer.decoder = decoders.ByteLevel()

    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        min_frequency=min_frequency,
        special_tokens=special_tokens,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        show_progress=not test_mode,
    )
    tokenizer.train_from_iterator(texts, trainer=trainer)
    return tokenizer


def save_tokenizer(tokenizer: Tokenizer, output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tokenizer_path = output_dir / "tokenizer.json"
    tokenizer.save(str(tokenizer_path), pretty=True)

    model_files = tokenizer.model.save(str(output_dir))
    contract = {
        "format": "laetex.tokenizer.contract/v1",
        "tokenizer_file": tokenizer_path.name,
        "model_files": [Path(path).name for path in model_files],
        "normalization": {"unicode": "identity", "line_endings": "preserve"},
        "pre_tokenizer": "ByteLevel(add_prefix_space=false,use_regex=true)",
        "decoder": "ByteLevel",
        "byte_fallback": True,
    }
    contract_path = output_dir / "tokenizer-contract.json"
    contract_path.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "tokenizer": str(tokenizer_path),
        "contract": str(contract_path),
        "model_files": ",".join(model_files),
    }
