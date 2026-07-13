# Phase 0 — Tokenizer and corpus

## Inputs and outputs

- **[VERIFIED FACT]** `T0-TOKENIZER` has no model-weight parent. It consumes a
  licensed, representative sample and emits immutable tokenizer files, special
  tokens, normalization rules, vocabulary and hashes.
- **[VERIFIED FACT]** `D0-CORPUS` emits versioned train/validation shards,
  curriculum, mixture weights and per-sample lineage bound to the tokenizer hash.
- **[RISK]** Evaluation/private tenant data are forbidden. Tenant opt-in requires
  separate consent, de-identification, namespace and revocation lineage.

## Gates

Tokenizer gates: byte roundtrip, frozen unknown-token limit, compression by
code/log/schema/language stratum, deterministic encoding and no eval
contamination. Corpus gates: license/consent coverage 100%, orphan samples zero,
PII/secrets review, exact/near dedup, split isolation and signed shard hashes.

## Compute contract

Canonical profile: `infra/runpod/profiles/tokenizer.yaml`. H200 only; local
tokenizer training is forbidden. External encrypted object storage is
authoritative. **[ENGINEERING HYPOTHESIS]** Throughput and wall-clock remain TBD
until a measured sample-to-shard pilot. No expensive proxy run starts until both
artifacts cold-load from a fresh allocation.
