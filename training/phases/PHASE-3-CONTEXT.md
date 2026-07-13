# Phase 3 — 32K, 128K and 256K context

## Sequence and profiles

`P0-PRETRAIN-8K → LC32K → LC128K → LC256K`

Profiles: `pretrain32k.yaml`, `long-context128k.yaml`,
`long-context256k.yaml`.

## Topology hypotheses

- 32K: 512=`8×8×8×1×1`; 1024=`8×8×8×2×1`.
- 128K: 512=`8×4×4×4×1`; 1024=`8×4×8×4×1`.
- 256K: 512=`8×2×4×8×1`; 1024=`8×2×8×8×1`.

Order is TP×PP×EP×CP×DP. **[RISK]** These are mathematically valid planning
points, not proven memory/throughput points. PP4/PP2 require architecture layer
divisibility and bubble proof. Keeping TP8/PP8/EP16 while adding CP would need
more than 1024 ranks and is therefore not a valid 1024-H200 claim.

## Curriculum and gates

Each stage mixes long sequences with short-context replay, freezes position/
attention changes before the expensive run and compares against structured
retrieval. Promotion requires context-specific retrieval, dependency reasoning
and state-tracking gains; short-context/code non-inferiority; memory, latency,
MFU and cold-restore success.

Stop if context gain is absent, structured state wins on verified tasks per
dollar, shorter capabilities regress beyond the frozen margin, or CP/fabric
efficiency misses its floor. Wall-clock is an **[ENGINEERING HYPOTHESIS]** until
measured at each sequence length.
