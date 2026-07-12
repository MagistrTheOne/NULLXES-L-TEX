# Phase 0 — Baseline до обучения

## Input, objective, output

- **[VERIFIED FACT] Input:** immutable Qwen3-Coder-Next-Base snapshot, неизменённый tokenizer, frozen LÆTEX-Bench draft, private held-out tasks, deterministic graders и cost schema.
- **[EXPERIMENT REQUIRED] Objective:** измерить исходные quality, latency, tool reliability, safety и cost до любого изменения весов.
- **[VERIFIED FACT] Output:** signed baseline manifest, per-task evidence, failed-task taxonomy, latency/cost distributions и contamination audit.
- **[RISK]** Нельзя использовать результат teacher или model judge как замену executable grader.

## Procedure

1. **[VERIFIED FACT]** Зафиксировать checkpoint/tokenizer/image/dataset/grader hashes.
2. **[EXPERIMENT REQUIRED]** Прогнать четыре трека LÆTEX-Bench с одинаковыми retry/tool budgets.
3. **[EXPERIMENT REQUIRED]** Измерить cold/warm TTFT, time-to-verified-change, pass-to-pass, recovery after injected tool failures и cost per verified task.
4. **[EXPERIMENT REQUIRED]** Выполнить identity/adversarial baseline, чтобы размер overwrite измерялся, а не предполагался.
5. **[VERIFIED FACT]** Replay 10% stratified tasks должен воспроизводить grader outcome.

## Exact success metric и stop condition

- **[VERIFIED FACT] Primary metric:** `VETCR = verified completed tasks / all eligible attempted tasks`; skipped/timeouts считаются failures.
- **[EXPERIMENT REQUIRED] Gate:** 100% task-attempt accounting, replay mismatch `0`, missing evidence `0`, contamination findings resolved; unweighted VETCR имеет Wilson 95% CI, а comparison plan — pre-registered stratified cluster bootstrap по task families.
- **[RISK] Stop:** checksum mismatch, grader nondeterminism вне frozen tolerance, утечка private eval в training namespace или любое изменение weights.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[EXPERIMENT REQUIRED]** Воспроизводимая baseline inference/evaluation без weight updates. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 16× H200 SXM 141 GB, два 8-GPU HGX-узла для baseline replay. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB, четыре HGX-узла для parallel replay. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** Min TP=4, PP=1, EP=1, CP=1, DP=4; rec DP=8; независимые TP replicas. |
| VRAM | **[VERIFIED FACT]** 141 GB HBM/GPU; BF16 reference weights; KV/cache budget измеряется на target context. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch внутри узла. **[RISK]** Для recommended multi-node требуется attested InfiniBand на RunPod `ens*`; публичные 3200 Gbps сами по себе этого не доказывают. |
| Storage | **[VERIFIED FACT]** `/workspace` Network Volume для working set; external encrypted object store для frozen inputs/evidence. |
| Checkpoint | **[VERIFIED FACT]** Weight checkpoints не создаются; сохраняются resumable task ledger и eval artifacts каждые 15 минут. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 12–36 часов для первого полного suite; уточнить после 100-task pilot. |
| Exact metric | **[VERIFIED FACT]** VETCR, Wilson 95% CI для unweighted rate, replay mismatch=0, audit completeness=100%. |
| Stop/economic justification | **[ENGINEERING HYPOTHESIS]** Full run оправдан только после frozen graders; 32 GPU — если wall-clock saving дешевле задержки решения. |
| Artifact | **[VERIFIED FACT]** `baseline-results`, replay bundle, cost/latency manifest, gate decision. |

## Risks

- **[RISK]** Small private suite даст широкий confidence interval; увеличить task count, а не скрывать uncertainty.
- **[RISK]** Long-context prompts могут превратить benchmark в I/O test; отдельно публиковать retrieval/context strata.
- **[RISK]** RunPod capacity/topology variance требует cluster acceptance report для каждого allocation.

