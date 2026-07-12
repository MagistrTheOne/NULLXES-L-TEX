# Phase 3 — Preference Optimization

## Input, objective, output

- **[VERIFIED FACT] Input:** accepted `M2` BF16, immutable pairs, `M2`-hash-bound cached reference log-probabilities, executable outcomes и disagreement records.
- **[ENGINEERING HYPOTHESIS] Objective:** предпочитать verified completion, минимальный достаточный action set, evidence-backed report, safe refusal/escalation и recovery.
- **[VERIFIED FACT] Output:** retained `A3`, BF16 `M3=M2+A3`, fresh optimizer record, pair lineage, KL/safety и merge parity.
- **[RISK]** Style-only preferences не являются enterprise outcome и должны иметь нулевой или низкий weight.

## Method selection

- **[EXPERIMENT REQUIRED]** Сравнить DPO и IPO на одинаковых pairs/compute; выбрать по VETCR–safety Pareto.
- **[VERIFIED FACT]** 480B checkpoint — foundation, не teacher. Отдельный critic отсутствует по умолчанию; pair label принимает executable verifier или human adjudication.
- **[ENGINEERING HYPOTHESIS]** Precompute reference log-probabilities, чтобы не держать вторую 480B policy resident.
- **[RISK]** Foundation self-preference создаёт bias; отчёт обязателен по source strata.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Gate:** held-out pair accuracy `>=65%`; VETCR `>=5% relative` к SFT; unsafe-action execution rate не выше SFT; protected coding regression `<=2 pp`; KL внутри frozen band.
- **[RISK] Stop:** safety worsens, KL band violated два evals, protected regression >2 pp или source-stratum inversion.
- **[ENGINEERING HYPOTHESIS]** Экономический gate: inter-rater agreement `>=0.8` либо executable adjudication; иначе сначала улучшить labels.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[ENGINEERING HYPOTHESIS]** Offline direct preference optimization adapter policy. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 64× H200 SXM 141 GB. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** 32: TP8/PP2/CP1/DP2/EP1; 64: TP8/PP2/CP2/DP2/EP1; base router/experts frozen. |
| VRAM | **[VERIFIED FACT]** 141 GB/GPU; cached reference log-probs уменьшают model residency, но требуют hash binding к SFT checkpoint. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Для recommended multi-node RunPod `ens*` допускается только с InfiniBand attestation; pair-order, NCCL/IB и distributed-loss parity test до run. |
| Storage | **[ENGINEERING HYPOTHESIS]** 4–8 TB Network Volume working set; durable encrypted registry для pairs/checkpoints/audit. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** `A3` + fresh optimizer/RNG/pair cursor каждые 500 steps/2 часа; retain `M2/A3/M3`. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 2–5 дней/method на 32; controlled DPO/IPO selection 3–8 дней на 64. |
| Exact metric | **[EXPERIMENT REQUIRED]** Pair accuracy >=65%, VETCR +5% relative, no safety increase, regression <=2 pp. |
| Stop/economic justification | **[RISK]** GPU run бессмысленен, если label disagreement не устранён или additional verified SFT дешевле. |
| Artifact | **[VERIFIED FACT]** `A3`, `M3` BF16, pair manifest, method-selection/merge/safety report. |

## Critic policy

- **[VERIFIED FACT]** Separate critic is `none` by default. Same upstream foundation cannot be relabeled as teacher.
- **[RISK]** Любой critic требует отдельного approval, checkpoint, H200 budget, evaluation stratum и lineage; он не выставляет final correctness label.
- **[VERIFIED FACT]** Stage 3 optimizer fresh; FP8 не может быть parent `M3`.

