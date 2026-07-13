# Custom tokenizer research contract

## Status and scope

- **VERIFIED FACT:** E-01 retains its upstream tokenizer and token IDs. This
  pipeline is not authorized to mutate an E-01 checkpoint.
- **ENGINEERING HYPOTHESIS:** A 128,000-token byte-level BPE may improve
  multilingual code and enterprise artifact compression for a future
  independently pretrained LÆTEX model.
- **EXPERIMENT REQUIRED:** Compare compression, downstream quality, latency, and
  embedding cost against the selected independent-model baseline before adoption.
- **RISK:** A custom vocabulary cannot be inserted into an existing checkpoint
  without retraining/adapting embeddings and the output head.

## Normative tokenizer contract

1. Algorithm: byte-level BPE, target vocabulary exactly 128,000 in production.
2. Coverage: complete 256-byte initial alphabet plus byte fallback.
3. Input encoding: strict UTF-8.
4. Normalization: identity. Unicode code points, whitespace, tabs, and CR/LF are
   preserved; NFC/NFKC and code rewriting are forbidden.
5. Round-trip: `decode(encode(text)) == text` on every held-out gate document.
6. Specials are atomic and have unique IDs:
   `<|bos|>`, `<|eos|>`, `<|pad|>`, `<|system|>`, `<|user|>`,
   `<|assistant|>`, `<|tool|>`, `<|tool_result|>`, `<|state|>`,
   `<|action|>`, `<|evidence|>`, `<|policy|>`, `<|repo|>`, `<|file|>`,
   `<|diff|>`.
7. Tokenizer, vocabulary, merges, config, source manifest, and validation report
   are content-hashed. A released model lineage pins those hashes.

Strict UTF-8 does not claim arbitrary binary-file round-trip. Binary assets stay
outside the tokenizer corpus. Text in legacy encodings must be transcoded
upstream with an append-only lineage record.

## Corpus and lineage gates

The JSON manifest schema requires per-source URI/type, approved license evidence,
PII status, secrets status, exact and near-duplicate policy, SHA-256 snapshot
hash, normalization contract, and the complete special-token list. Production
sampling fails closed on missing approval metadata or source hash mismatch.

No real corpus is stored here. Tenant data is not accepted by default; any future
tenant-derived source requires a separate explicit-consent and isolation policy
before it can satisfy `training_allowed=true`.

## RunPod-only production procedure

Real corpus processing and BPE training run only in a RunPod job with:

- an immutable package/config/schema checkout;
- an isolated encrypted corpus volume mounted under `/workspace`;
- a reviewed manifest whose `local_path` values resolve only inside that volume;
- `RUNPOD_POD_ID` injected by the platform;
- artifact upload to versioned object storage after hash verification.

The pipeline itself is CPU/RAM intensive and does not require model weights.
RunPod remains mandatory because the project compute/data boundary forbids real
training workloads on local machines. Size CPU and RAM from a corpus pilot; do
not infer tokenizer throughput from the synthetic smoke test.

## Local test exception

Local execution requires both `--execution-mode test` and `--test-mode`. It
ignores all external sources, rejects any manifest `local_path`, generates a
fixed synthetic fixture, and enforces a hard aggregate limit of 1 MiB. Its only
purpose is contract and packaging validation; its vocabulary size and
compression metrics are not research results.

## Required production outputs

- `tokenizer.json`
- `vocab.json` and `merges.txt`
- `tokenizer-contract.json`
- `training-attestation.json` with source/config hashes, special IDs,
  round-trip count, compression metrics, execution identity, and artifact hashes
