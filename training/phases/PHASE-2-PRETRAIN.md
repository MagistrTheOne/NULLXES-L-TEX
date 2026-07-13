# Phase 2 — Target initialization and 8K pretraining

## Lineage

`ARCH-FREEZE + T0-TOKENIZER + D0-CORPUS → I0-INIT → P0-PRETRAIN-8K`

`I0-INIT` creates every target tensor from a signed seed and initialization
contract. **[VERIFIED FACT]** External and proxy weights are forbidden.

## H200 plan

- Minimum campaign envelope: 512 H200, 64 homogeneous 8-GPU HGX nodes.
- Recommended: 1024 H200, 128 nodes.
- 512 layout: `TP8×PP8×EP8×CP1×DP1=512`.
- 1024 layout: `TP8×PP8×EP16×CP1×DP1=1024`; with 144 routed experts,
  `144/16=9` experts per EP rank.

**[RISK]** 512 cannot realize independent TP8/PP8/EP16. The EP8 fallback must
pass memory, all-to-all, routing and quality parity; otherwise target pretraining
requires 1024.

## Training and gates

Full-parameter next-token pretraining uses a BF16 master. Transformer Engine FP8
compute is optional only after proxy numerical parity; FP8 checkpoints do not
replace the BF16 master. Track consumed tokens, loss, gradient norm, MFU, router
entropy/load, expert utilization, dropped tokens, all-to-all time and data mix.

Stop on sustained divergence, non-finite values, router collapse, lineage gap,
fabric fallback, checkpoint cold-restore failure or violation of the frozen
budget. **[ENGINEERING HYPOTHESIS]** Token budget and wall-clock are determined
from ARCH-FREEZE scaling evidence and achieved throughput, not declared here.
