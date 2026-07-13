# LÆTEX E-01: from-scratch training program

## Canonical lanes

Proxy lane:
`PX1-1B → PX2-7B → PX3-30B → ARCH-FREEZE`.

Target lane:
`T0-TOKENIZER → D0-CORPUS → I0-INIT → P0-PRETRAIN-8K → LC32K → LC128K →
LC256K → SFT → PREF → GRPO → R1-BF16 → FP8`.

**[VERIFIED FACT]** Proxy weights, optimizer state and checkpoint shards cannot
parent target training. Target weights originate only at `I0-INIT` from the
signed architecture, tokenizer, seed and initialization contract.

## Program phases

1. [`PHASE-0-TOKENIZER-DATA.md`](phases/PHASE-0-TOKENIZER-DATA.md): tokenizer
   and corpus governance.
2. [`PHASE-1-PROXIES.md`](phases/PHASE-1-PROXIES.md): 1B/7B/30B scaling and
   systems evidence; architecture freeze.
3. [`PHASE-2-PRETRAIN.md`](phases/PHASE-2-PRETRAIN.md): new target
   initialization and 8K pretraining.
4. [`PHASE-3-CONTEXT.md`](phases/PHASE-3-CONTEXT.md): 32K→128K→256K.
5. [`PHASE-4-POSTTRAIN.md`](phases/PHASE-4-POSTTRAIN.md): SFT→PREF→GRPO.
6. [`PHASE-6-RELEASE.md`](phases/PHASE-6-RELEASE.md): R1-BF16 qualification and
   FP8 derivative.

## Hard constraints

- **[VERIFIED FACT]** H200 only. Target planning is 512 minimum / 1024
  recommended; no local tokenizer/model training, inference or trajectory
  generation.
- **[RISK]** Provider-attested NVLink/NVSwitch and InfiniBand plus NCCL
  all-to-all acceptance are allocation gates.
- **[VERIFIED FACT]** External encrypted object storage is the source of truth;
  RunPod volumes are replaceable working sets.
- **[ENGINEERING HYPOTHESIS]** `TP8/PP8/EP16` requires 1024 ranks at CP1/DP1.
  512 uses explicit fallback topology. Long-context stages trade PP/EP for CP;
  all arithmetic is in profile manifests.
- **[ENGINEERING HYPOTHESIS]** Wall-clock, MFU, throughput, token budgets and
  costs are unknown until measured. No run is authorized by documentation alone.

## Promotion contract

Every run records code/image/profile/data/tokenizer/parent hashes, exact
`TP×PP×EP×CP×DP`, allocation/fabric evidence, optimizer/scheduler/RNG state,
consumed tokens, checkpoint cold restore, eval outputs, cost and signed
promotion decision. A failed or incomplete gate cannot become a parent.

