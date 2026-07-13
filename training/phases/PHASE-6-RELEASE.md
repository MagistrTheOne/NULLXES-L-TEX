# Phase 6 — BF16 release and FP8 derivative

## R1-BF16

`GRPO → R1-BF16` freezes an immutable BF16 master. Training is disabled.
Qualification runs on 512 H200 minimum / 1024 recommended and requires two clean
runs of frozen LÆTEX-Bench, pretrain/coding regression, long-context,
security/governance red-team and tool-failure replay.

Hard gates: critical security or destructive-action findings zero, replay
mismatch zero, audit/lineage completeness 100%, cold load from the external
object-store source of truth and signed immutable hashes. Human release authority
owns promotion.

## FP8

`R1-BF16 → FP8` is an inference-only conversion. FP8 never becomes a training
parent and never replaces the BF16 source of truth. Promotion requires conversion
and calibration lineage, load success, task/safety parity and measured memory,
latency and cost improvement.

## Infrastructure honesty

Canonical profiles are `bf16-release.yaml` and `fp8-export.yaml`. Exact
`TP×PP×EP×CP×DP` arithmetic is recorded in them. **[ENGINEERING HYPOTHESIS]**
Wall-clock and serving economics remain unknown until immutable-suite throughput
is measured. No provisioning, training, conversion or release is performed by
these contracts.
