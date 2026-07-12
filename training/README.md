# LÆTEX E-01: direct 480B foundation program

## Неподвижные ограничения

- **[VERIFIED FACT]** Foundation и production candidate — `Qwen/Qwen3-Coder-480B-A35B-Instruct`. 80B student и отдельный 480B teacher удалены.
- **[VERIFIED FACT]** Тот же upstream checkpoint нельзя называть teacher. Отдельный critic отсутствует по умолчанию и требует отдельного approval/checkpoint/lineage.
- **[VERIFIED FACT]** Только NVIDIA H200 SXM 141 GB в RunPod Secure Cloud; локальные model workloads запрещены.
- **[VERIFIED FACT]** BF16 masters являются единственными training/merge parents; FP8 — только release export после parity.
- **[RISK]** Следующая фаза стартует только по подписанному gate предыдущей.

## Gate sequence

| Phase | Назначение | Master output |
|---|---|---|
| 0 | Baseline direct upstream foundation | Frozen baseline; weights unchanged |
| 1 | Identity/tool BF16 LoRA; broad CPT disabled | `A1` retained; `M1=U0+A1` BF16 |
| 2 | Enterprise Action SFT LoRA | `A2` retained; `M2=M1+A2` BF16 |
| 3 | DPO/IPO method selection | `A3` retained; `M3=M2+A3` BF16 |
| 4 | Conditional executable GRPO | `A4` retained; `M4=M3+A4` BF16 |
| 5 | Separate adapter router / optional World Model V1 | Independent auxiliary artifacts; no merge into `M4` |
| 6 | BF16 release gate and optional FP8 parity | Signed BF16 bundle; optional FP8 export |

## Method policy

- **[ENGINEERING HYPOTHESIS]** Default E-01 path: dense attention-projection BF16 LoRA with base MoE router and 160 routed experts frozen in Phases 1–4.
- **[RISK]** Broad CPT is disabled. `PHASE-1-CPT.md` is retained only for cross-link compatibility and documents Stage 1 plus optional separately approved DAPT ablation.
- **[VERIFIED FACT]** Every merge retains adapter and pre-merge parent; post-merge load/protected eval is mandatory.
- **[VERIFIED FACT]** Optimizer/scheduler state is fresh at every stage and never crosses `M1/M2/M3/M4` merge boundaries.
- **[RISK]** Full-parameter 480B tuning is not E-01; minimum planning envelope is `>=128 H200` only after optimizer/checkpoint memory proof.
- **[RISK]** QLoRA and FP8 training are not defaults. FP8 cannot parent training or merge.

## H200 envelope

- **[ENGINEERING HYPOTHESIS]** Baseline: 16/32 H200.
- **[ENGINEERING HYPOTHESIS]** Identity and Action LoRA: 16/32 at 8–16K; 64 recommended at 32–64K.
- **[ENGINEERING HYPOTHESIS]** Preference: 32/64. GRPO: 64/128; 128 requires RunPod sales capacity beyond standard 64.
- **[ENGINEERING HYPOTHESIS]** Release BF16: 16/32. FP8 candidate: 8/16 only after parity.

## Reproducibility contract

Каждый run manifest фиксирует Git/image/profile hashes; parent/adapter/output hashes; tokenizer/template/tool schema; data lineage; exact `world_size/TP/PP/CP/DP/EP`; optimizer freshness; RunPod allocation и network attestation; checkpoints; wall-clock/cost; graders и promotion decision.

- **[VERIFIED FACT]** `world_size=TP×PP×CP×DP`; EP валидируется отдельно и не умножается повторно.
- **[VERIFIED FACT]** Network Volume — working set; external encrypted object store — durable source of truth.
- **[ENGINEERING HYPOTHESIS]** Все wall-clock ranges — hypotheses до measured pilot throughput.
- **[RISK]** Экономический gate — cost per incremental verified task, не training loss.

