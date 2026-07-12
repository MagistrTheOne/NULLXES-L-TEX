# Phase 2 — Enterprise Action SFT

## Canonical profiles and lineage position

- **[VERIFIED FACT]** Action `A2`: [`../../infra/runpod/profiles/sft.yaml`](../../infra/runpod/profiles/sft.yaml).
- **[VERIFIED FACT]** Separate BF16 merge `M2`: [`../../infra/runpod/profiles/merge-m2.yaml`](../../infra/runpod/profiles/merge-m2.yaml).
- **[VERIFIED FACT]** Strict position: accepted `M1 → A2 → M2`; preference `A3` consumes only promoted `M2`.
- **[RISK]** Missing, unsigned or hash-unpinned train/merge profile blocks the job. No run or gate pass is claimed here.

## Input, objective, output

- **[VERIFIED FACT] Input:** accepted `M1` BF16, unchanged tokenizer, LÆTEX contracts, verified action examples и protected replay.
- **[ENGINEERING HYPOTHESIS] Objective:** обучить enterprise action behavior, evidence discipline, tool recovery и escalation policy.
- **[VERIFIED FACT] Output contract:** retained `A2`, then BF16 `M2=M1+A2`, fresh optimizer record, merge parity и task evidence.
- **[RISK]** Generic synthetic conversations без executable evidence размоют coding behavior и не должны доминировать.

## Training recipe

- **[ENGINEERING HYPOTHESIS]** Default — BF16 LoRA на dense attention projections; base MoE router и 160 routed experts frozen.
- **[ENGINEERING HYPOTHESIS]** Initial target — 180k–300k verified examples; общий ActionWorld target отдельно включает 60k–120k executable trajectories и 20k–60k failure/recovery trajectories.
- **[VERIFIED FACT]** Every tool trajectory содержит initial state hash, action, observed delta, tests/policy evidence и final status.
- **[ENGINEERING HYPOTHESIS]** Mix: construction, architecture, integrations, DevOps/SRE, security, QA, communication, governance плюс 20–30% protected coding replay.
- **[RISK]** Foundation self-generation не является teacher evidence. Отдельный critic требует approval; все synthetic examples проходят executable/human gate.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Gate:** VETCR `>=10% relative` к `M1`; schema validity `>=99.5%`; identity leakage `0/10,000`; coding regression `<=2 pp`; evidence `>=98%`.
- **[RISK] Stop:** identity leakage в release-candidate eval, validation deterioration два раза, schema validity <99%, или coding regression >2 pp.
- **[ENGINEERING HYPOTHESIS]** Экономический gate: accepted-example rate >=90%, а one-epoch pilot показывает положительный VETCR slope.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[ENGINEERING HYPOTHESIS]** Enterprise Action BF16 LoRA on `M1`. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 16× H200 для 8–16K. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 для 8–16K; 64× для 32–64K. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** 16: TP8/PP2/CP1/DP1/EP1; 32: TP8/PP2/CP1/DP2/EP1; 64: TP8/PP2/CP2/DP2/EP1. |
| VRAM | **[ENGINEERING HYPOTHESIS]** BF16 `M1` sharded; adapter/optimizer separately sharded; CP required for long-context proof. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Для recommended multi-node RunPod `ens*` должен быть attested как InfiniBand; NCCL/IB и dataloader acceptance обязательны. |
| Storage | **[ENGINEERING HYPOTHESIS]** 4 TB min / 8 TB rec Network Volume; encrypted object store хранит immutable examples и release candidates. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** `A2` + optimizer/RNG/cursor каждые 500 steps/2 часа; retain `M1/A2/M2`; load/eval after merge. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 8–16K: 3–8 дней/16 или 2–5/32; 32–64K: 3–8/64 после pilot. |
| Exact metric | **[EXPERIMENT REQUIRED]** VETCR +10% relative, identity 0/10k, schema >=99.5%, regression <=2 pp. |
| Stop/economic justification | **[RISK]** Не масштабировать, если additional verified data улучшает VETCR дешевле GPU scaling или если pilot slope нулевой. |
| Artifact | **[VERIFIED FACT]** `A2`, `M2` BF16, merge lineage, action/evidence/capability reports. |

## Identity controls

- **[VERIFIED FACT]** User-facing identity — LÆTEX; internal model card сохраняет происхождение и license notices.
- **[RISK]** Архитектурное происхождение и inherited representations не «стираются»; запрещено утверждать pretraining from zero.
- **[EXPERIMENT REQUIRED]** Проверить self-identification, indirect extraction, multilingual prompts, role conflicts, tool error paths и long-context identity drift.
- **[VERIFIED FACT]** Stage 2 uses a fresh optimizer; Stage 1 optimizer state is not resumed. FP8 cannot parent `M2`.
- **[VERIFIED FACT]** `A2` training и `M2` merge — separate H200 jobs; local model training/merge workloads запрещены.

