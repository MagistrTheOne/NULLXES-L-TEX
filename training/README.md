# LÆTEX E-01: canonical training lineage

## Неподвижные ограничения

- **[VERIFIED FACT]** Foundation и production candidate — `Qwen/Qwen3-Coder-480B-A35B-Instruct`. 80B student и отдельный 480B teacher удалены.
- **[VERIFIED FACT]** Тот же upstream checkpoint нельзя называть teacher. Отдельный critic отсутствует по умолчанию и требует отдельного approval/checkpoint/lineage.
- **[VERIFIED FACT]** Только NVIDIA H200 SXM 141 GB в RunPod Secure Cloud; локальные model workloads запрещены.
- **[VERIFIED FACT]** Frozen BF16 source master называется `S0`; обозначение `U0` в training-контракте запрещено.
- **[VERIFIED FACT]** BF16 masters являются единственными training/merge parents; FP8 — только release export после parity.
- **[RISK]** Следующая фаза стартует только по подписанному gate предыдущей.
- **[VERIFIED FACT]** Локальные training, inference, merge, CPT/DAPT, RL и teacher-generation workloads запрещены; local control plane хранит только код, конфиги и обезличенные metadata.

## Строгая canonical sequence

`S0 → identity A1 → merge M1 → action A2 → merge M2 → preference A3 → merge M3 → GRPO A4 → merge M4 → FP8 parity/export → release eval`

| Phase | Training action | Required canonical profiles | Output |
|---|---|---|---|
| 0 | Freeze and baseline `S0`; weights unchanged | [`baseline.yaml`](../infra/runpod/profiles/baseline.yaml) | Signed `S0` baseline evidence |
| 1 | Identity/tool `A1`; broad CPT disabled | [`identity-lora.yaml`](../infra/runpod/profiles/identity-lora.yaml), [`merge-m1.yaml`](../infra/runpod/profiles/merge-m1.yaml); optional disabled DAPT contract: [`cpt-disabled.yaml`](../infra/runpod/profiles/cpt-disabled.yaml) | `A1`, then verified BF16 `M1=S0+A1` |
| 2 | Enterprise Action SFT `A2` | [`sft.yaml`](../infra/runpod/profiles/sft.yaml), [`merge-m2.yaml`](../infra/runpod/profiles/merge-m2.yaml) | `A2`, then verified BF16 `M2=M1+A2` |
| 3 | Preference optimization `A3` | [`preference.yaml`](../infra/runpod/profiles/preference.yaml), [`merge-m3.yaml`](../infra/runpod/profiles/merge-m3.yaml) | `A3`, then verified BF16 `M3=M2+A3` |
| 4 | Conditional executable GRPO `A4` | [`grpo.yaml`](../infra/runpod/profiles/grpo.yaml), [`merge-m4.yaml`](../infra/runpod/profiles/merge-m4.yaml) | `A4`, then verified BF16 `M4=M3+A4` |
| 5 | Independent router / optional World Model V1 | [`router-world-model.yaml`](../infra/runpod/profiles/router-world-model.yaml) | Auxiliary artifacts only; canonical policy lineage remains `M4` |
| 6 | FP8 parity/export, then release evaluation | [`fp8-export.yaml`](../infra/runpod/profiles/fp8-export.yaml), затем [`release-eval.yaml`](../infra/runpod/profiles/release-eval.yaml) | Signed FP8 derivative or reject; release/reject evidence |

- **[VERIFIED FACT]** Profile order is part of the lineage contract; train and merge are separate jobs.
- **[RISK]** Missing, unsigned or hash-unpinned canonical profile blocks the job. This document does not assert that a profile exists, a run occurred or a gate passed.
- **[VERIFIED FACT]** Phase 5 may execute only as a separately approved auxiliary branch and cannot reorder or parent the canonical `S0→M4→FP8→release-eval` lineage.

## Method policy

- **[ENGINEERING HYPOTHESIS]** Default E-01 path: dense attention-projection BF16 LoRA with base MoE router and 160 routed experts frozen in Phases 1–4.
- **[RISK]** Broad CPT is disabled. `PHASE-1-CPT.md` remains only as a compatibility filename; default Phase 1 uses `identity-lora.yaml`. Optional DAPT points to `cpt-disabled.yaml` and cannot run until a separate approval explicitly replaces its disabled state.
- **[VERIFIED FACT]** Every merge uses its dedicated canonical merge profile, retains adapter and pre-merge parent, and requires post-merge load/protected parity before promotion.
- **[VERIFIED FACT]** Optimizer/scheduler state is fresh at every stage and never crosses `M1/M2/M3/M4` merge boundaries.
- **[RISK]** Full-parameter 480B tuning is not E-01; minimum planning envelope is `>=128 H200` only after optimizer/checkpoint memory proof.
- **[RISK]** QLoRA and FP8 training are not defaults. FP8 cannot parent training or merge.

## H200 envelope

- **[ENGINEERING HYPOTHESIS]** Baseline: 16/32 H200.
- **[ENGINEERING HYPOTHESIS]** Identity and Action LoRA: 16/32 at 8–16K; 64 recommended at 32–64K.
- **[ENGINEERING HYPOTHESIS]** Preference: 32/64. GRPO: 64/128; 128 requires RunPod sales capacity beyond standard 64.
- **[ENGINEERING HYPOTHESIS]** Release BF16: 16/32 H200. FP8 candidate: 8/16 H200; export promotion occurs only after parity.

## Reproducibility contract

Каждый proposed run manifest должен фиксировать Git/image/profile hashes; parent/adapter/output hashes; tokenizer/template/tool schema; data lineage; exact `world_size/TP/PP/CP/DP/EP`; optimizer freshness; RunPod allocation и network attestation; checkpoints; wall-clock/cost; graders и promotion decision.

- **[VERIFIED FACT]** `world_size=TP×PP×CP×DP`; EP валидируется отдельно и не умножается повторно.
- **[VERIFIED FACT]** Network Volume — working set; external encrypted object store — durable source of truth.
- **[ENGINEERING HYPOTHESIS]** Все wall-clock ranges — hypotheses до measured pilot throughput.
- **[RISK]** Экономический gate — cost per incremental verified task, не training loss.

