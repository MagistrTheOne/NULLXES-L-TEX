# ADR-0008: Custom tokenizer for E-01

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Дата: 2026-07-13.
- **VERIFIED FACT:** Область: independent from-scratch E-01.

## Решение

- **VERIFIED FACT:** E-01 получает собственный tokenizer, обученный до model pretraining; vocabulary target — 128K.
- **VERIFIED FACT:** Никакой tokenizer, vocabulary или token-ID mapping Qwen не наследуется.
- **ENGINEERING HYPOTHESIS:** Corpus-balanced byte-fallback BPE или Unigram является стартовым candidate; окончательный algorithm выбирается измерением compression, code fidelity, multilingual coverage и runtime cost.
- **ENGINEERING HYPOTHESIS:** Special-token contract резервируется до tokenizer freeze для documents, tools, state/evidence boundaries и post-training roles.

## Gates

- **EXPERIMENT REQUIRED:** Сравнить candidates на frozen multilingual/code/enterprise holdouts по bytes-per-token, tokens-per-artifact, round-trip integrity, unknown-byte behavior и downstream proxy loss.
- **EXPERIMENT REQUIRED:** Tokenizer hash, normalization, trainer config, corpus manifest и special-token map должны быть immutable parents всех pretraining checkpoints.
- **RISK:** Изменение tokenizer после начала pretraining создаёт новый lineage; silent mutation или remap запрещены.
- **RISK:** 128K vocabulary увеличивает embedding/output parameters и communication; tying policy и exact parameter impact должны войти в proxy validation.

## Supersession

- **VERIFIED FACT:** Этот ADR supersedes ADR-0001, который относился к отменённому derivative design.
