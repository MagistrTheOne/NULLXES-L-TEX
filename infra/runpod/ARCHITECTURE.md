# RunPod architecture: independent from-scratch E-01

## Compute boundary

- **[VERIFIED FACT]** Все model training, model inference, tokenizer training и
  trajectory generation выполняются только на homogeneous NVIDIA H200 HGX.
  Локальная машина — control plane без weights, train shards и model workloads.
- **[ENGINEERING HYPOTHESIS]** Target campaign: 512 H200 minimum, 1024 H200
  recommended. Эти числа — planning envelopes, не подтверждение capacity,
  throughput, affordability или RunPod availability.
- **[RISK]** До reservation конкретный allocation обязан получить письменную
  provider attestation NVLink/NVSwitch intra-node и InfiniBand inter-node, затем
  пройти NCCL collective/all-to-all, GPU health, storage и checkpoint-resume
  acceptance. Marketing bandwidth не является attestation.

## Canonical lineage

`T0-TOKENIZER → D0-CORPUS → I0-INIT → P0-PRETRAIN-8K → LC32K → LC128K →
LC256K → SFT → PREF → GRPO → R1-BF16 → FP8`

Proxy lane `PX1-1B → PX2-7B → PX3-30B → ARCH-FREEZE` передаёт target lane только
спецификации и evidence. Proxy weights/optimizer/checkpoints запрещены как
target parents.

## Parallelism arithmetic

Для профилей используется явная независимая размерность:

`world_size = TP × PP × EP × CP × DP`

**[ENGINEERING HYPOTHESIS]** Preferred target point `TP8/PP8/EP16` корректен
только при world size не меньше `8×8×16=1024` для `CP1/DP1`. При 144 routed
experts `144/16=9` experts на EP rank.

**[RISK]** 512 H200 не реализуют одновременно независимые `TP8/PP8/EP16`.
Canonical 512 fallback для 8K использует `TP8/PP8/EP8/CP1/DP1`; long-context
profiles уменьшают PP/EP, чтобы добавить CP и сохранить world-size arithmetic.
`ARCH-FREEZE` обязан подтвердить layer divisibility, bubble cost, memory fit и
что fallback не меняет quality. Нельзя скрыто считать EP частью DP.

## Phase mappings

- 8K: 512=`8×8×8×1×1`; 1024=`8×8×16×1×1`.
- 32K: 512=`8×8×8×1×1`; 1024=`8×8×8×2×1`.
- 128K: 512=`8×4×4×4×1`; 1024=`8×4×8×4×1`.
- 256K: 512=`8×2×4×8×1`; 1024=`8×2×8×8×1`.
- Post-train/release defaults return to 8K/32K layouts; exact rollout/inference
  rank partitions are recorded separately and sum to world size.

## Storage and checkpoint contract

- External encrypted, versioned object storage is the durable source of truth
  for datasets, tokenizer, architecture freeze, BF16 checkpoints, optimizer/RNG
  state, FP8 export and evidence.
- RunPod Network Volume is a replaceable working set; node-local NVMe is
  ephemeral cache. Every download/upload is hash-verified.
- Pretrain checkpoints include model, distributed optimizer, scheduler, RNG,
  dataloader cursor, consumed-token counters and topology transform metadata.
  Cadence is time- and token-based, finalized by measured write/resume SLO.
- A run cannot promote without cold restore on a fresh allocation.

## Profiles and economics

Canonical profiles are exactly tokenizer, proxy1/7/30, target-init,
pretrain8k/32k, long-context128k/256k, sft, preference, grpo, bf16-release and
fp8-export. Historical derivative contracts are outside `profiles/`.

**[ENGINEERING HYPOTHESIS]** Every wall-clock, MFU, throughput, storage-volume
and cost claim is provisional until measured. Full-scale H200 execution is
economically allowed only after its predecessor proves data readiness,
checkpoint recovery, network efficiency, frozen stop conditions and expected
quality gain per H200-hour. This repository provisions and trains nothing.

