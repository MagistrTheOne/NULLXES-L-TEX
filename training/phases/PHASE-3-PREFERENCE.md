# Phase 3 — Preference Optimization

## Input, objective, output

- **[VERIFIED FACT] Input:** accepted SFT policy, immutable chosen/rejected pairs, cached reference log-probabilities, executable outcomes, policy labels и disagreement records.
- **[ENGINEERING HYPOTHESIS] Objective:** предпочитать verified completion, минимальный достаточный action set, evidence-backed report, safe refusal/escalation и recovery.
- **[VERIFIED FACT] Output:** preference adapter/checkpoint, pair lineage, KL/safety curves и adjudication report.
- **[RISK]** Style-only preferences не являются enterprise outcome и должны иметь нулевой или низкий weight.

## Method selection

- **[EXPERIMENT REQUIRED]** Сравнить DPO, IPO и ORPO на одинаковых pairs/compute; выбрать по VETCR–safety Pareto, не по training loss.
- **[VERIFIED FACT]** Teacher 480B может offline предлагать кандидатов/critique, но pair label принимается executable verifier или human adjudication.
- **[ENGINEERING HYPOTHESIS]** Precompute reference log-probabilities, чтобы не держать вторую 80B policy в training memory.
- **[RISK]** Pair imbalance и teacher self-preference создают reward bias; отчёт обязателен по source strata.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Gate:** held-out pair accuracy `>=65%`; VETCR `>=5% relative` к SFT; unsafe-action execution rate не выше SFT; protected coding regression `<=2 pp`; KL внутри frozen band.
- **[RISK] Stop:** safety worsens, KL band violated два evals, protected regression >2 pp или source-stratum inversion.
- **[ENGINEERING HYPOTHESIS]** Экономический gate: inter-rater agreement `>=0.8` либо executable adjudication; иначе сначала улучшить labels.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[ENGINEERING HYPOTHESIS]** Offline direct preference optimization adapter policy. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 8× H200 SXM 141 GB, один Secure Cloud HGX Pod для одного method pilot. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB, 4 узла для parallel method ablation. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** Min TP=2, PP=1, EP=4, CP=1, DP=4; rec TP=2, PP=1, EP=8, CP=1, DP=16. |
| VRAM | **[VERIFIED FACT]** 141 GB/GPU; cached reference log-probs уменьшают model residency, но требуют hash binding к SFT checkpoint. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Для recommended multi-node RunPod `ens*` допускается только с InfiniBand attestation; pair-order, NCCL/IB и distributed-loss parity test до run. |
| Storage | **[ENGINEERING HYPOTHESIS]** 4–8 TB Network Volume working set; durable encrypted registry для pairs/checkpoints/audit. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** Каждые 500 steps/2 часа; last-3 + best VETCR/safety Pareto; pair cursor сохраняется. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 1–4 дня на method, 3–8 дней для controlled three-method ablation. |
| Exact metric | **[EXPERIMENT REQUIRED]** Pair accuracy >=65%, VETCR +5% relative, no safety increase, regression <=2 pp. |
| Stop/economic justification | **[RISK]** GPU run бессмысленен, если label disagreement не устранён или additional verified SFT дешевле. |
| Artifact | **[VERIFIED FACT]** Preference bundle, pair manifest, method-selection and safety report. |

## Offline teacher sub-job

- **[VERIFIED FACT]** Teacher Qwen3-Coder-480B-A35B-Instruct: 480B total / 35B activated; только offline.
- **[ENGINEERING HYPOTHESIS]** Minimum 16 H200, recommended 32 H200 для BF16 teacher inference; TP=8, PP=2/4, DP=1; фактический mapping валидируется memory/load test.
- **[RISK]** Teacher generation — отдельный budget и artifact; она не входит в live policy path и не может сама выставить final correctness label.

