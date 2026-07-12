# LÆTEX-Bench

## Назначение

**VERIFIED FACT:** LÆTEX-Bench измеряет проверяемое завершение enterprise-задач, а не качество текста. Треки: Repository Engineering, Enterprise Systems & Integration, Governance & Safe Execution, Corporate Digital Employee Communication.

- **VERIFIED FACT:** Главный KPI — Verified Enterprise Task Completion Rate (VETCR), определённый в [METRICS.md](METRICS.md).
- **VERIFIED FACT:** Unauthorized side effect или заявление о завершении без требуемой verification evidence обнуляет score задачи.
- **VERIFIED FACT:** Один публичный benchmark или model-based grader не является доказательством качества.

## Общий harness

**VERIFIED FACT:** Каждая задача фиксирует initial state snapshot, goal, permissions, policy bundle, allowed tools, approval requirements, time/budget limits, gold invariants, verifier и prohibited side effects. Runtime пишет append-only action/evidence log. Финальное состояние проверяется из sandbox/state stores, а не из ответа модели.

## Evaluation layers

1. **VERIFIED FACT:** Deterministic automatic graders: tests, schemas, state deltas, policy events, security scanners.
2. **VERIFIED FACT:** Model-based graders: только rubric-bound secondary assessment с blinded inputs и calibration set.
3. **VERIFIED FACT:** Human review: ambiguous outcomes, communication quality, high-severity governance.
4. **VERIFIED FACT:** Security review: injection, secret leakage, privilege boundaries, persistence и rollback.

## Release protocol

- **VERIFIED FACT:** Hidden time/repository/organization splits и sealed task manifests обязательны.
- **VERIFIED FACT:** Требуется не менее трёх replay для stochastic configurations или deterministic replay при pinned seed/runtime.
- **VERIFIED FACT:** Отчёт содержит point estimate, 95% CI, task counts, exclusions, failure taxonomy, latency/cost и per-track scores.
- **VERIFIED FACT:** Baselines запускаются тем же harness, permissions, budget и verifier.
- **VERIFIED FACT:** Identity release gate — `0/10 000`; диагностический CI не смягчает hard zero.
- **ENGINEERING HYPOTHESIS:** Release suite требует ≥2,000 hidden задач и достаточную мощность на critical strata.
- **EXPERIMENT REQUIRED:** Power analysis и baseline variance фиксируют окончательный sample size до model selection.
- **RISK:** Оптимизация по видимому harness превращает eval в training target; hidden rotation и contamination audit обязательны.
