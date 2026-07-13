# LÆTEX tokenizer pipeline

This package implements the tokenizer contract for the independent LÆTEX research
line. It does **not** replace the frozen upstream tokenizer used by E-01.

The target is a 128,000-token byte-level BPE with an identity Unicode normalizer,
a complete byte alphabet, and explicit round-trip and special-token gates.

## Execution boundary

- Real corpus sampling and tokenizer training are permitted only on RunPod.
- The production command requires `RUNPOD_POD_ID` and `--execution-mode runpod`.
- A workstation may run only `--execution-mode test --test-mode`; that path uses
  a generated synthetic fixture, rejects configured corpus sources, and enforces
  a hard 1 MiB input limit.
- This repository contains no real training corpus.

Install the package in a RunPod job image:

```bash
python -m pip install /workspace/repo/packages/laetex-tokenizer
laetex-tokenizer \
  --config /workspace/repo/configs/e01/tokenizer/train-128k.yaml \
  --manifest /workspace/manifests/tokenizer-corpus.v1.json \
  --schema /workspace/repo/schemas/laetex-tokenizer-manifest.v1.json \
  --output /workspace/artifacts/tokenizer-v1 \
  --execution-mode runpod
```

Local synthetic contract smoke test:

```bash
laetex-tokenizer \
  --config configs/e01/tokenizer/train-128k.yaml \
  --manifest configs/e01/tokenizer/synthetic-test-manifest.json \
  --schema schemas/laetex-tokenizer-manifest.v1.json \
  --output .tmp/tokenizer-smoke \
  --execution-mode test --test-mode
```

The smoke tokenizer can be smaller than 128,000 because a sub-1 MiB synthetic
fixture cannot produce a representative 128k vocabulary. Production mode fails
unless the realized vocabulary is exactly 128,000.
