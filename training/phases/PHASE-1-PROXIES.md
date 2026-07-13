# Phase 1 — Proxy scaling and architecture freeze

## Sequence

`PX1-1B → PX2-7B → PX3-30B → ARCH-FREEZE`

Profiles: `proxy1.yaml`, `proxy7.yaml`, `proxy30.yaml`.

**[VERIFIED FACT]** Every proxy is initialized from scratch. A later proxy may
consume earlier measurements and tested code, but not earlier weights unless its
own approved experiment explicitly says so. No proxy weight, optimizer state or
checkpoint shard can enter target lineage.

## Objectives

- PX1 validates tokenizer integration, packing, optimizer, loss, determinism and
  exact checkpoint/resume.
- PX2 fits scaling curves and tests μP/initialization/optimizer transfer
  hypotheses.
- PX3 tests target-like MoE routing, hybrid attention, expert all-to-all,
  checkpoint transforms and failure recovery.
- ARCH-FREEZE signs exact architecture and parameter arithmetic, 144-expert
  routing decision, token budget, curriculum and every topology.

## Stop and economic gates

Stop on unstable loss/gradients, data accounting gap, resume mismatch, router
collapse, fabric failure or scaling residual outside preregistered tolerance.
**[ENGINEERING HYPOTHESIS]** Wall-clock and quality-per-compute are measured
outputs, not planning facts. Each larger proxy must answer a decision that the
smaller proxy cannot answer cheaper.
