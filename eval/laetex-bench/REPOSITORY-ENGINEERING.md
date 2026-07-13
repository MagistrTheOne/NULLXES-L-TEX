# Track 1: Repository Engineering

## Tasks

**[VERIFIED FACT]** Contract task classes: bug fix, cross-module feature, invariant-preserving refactor, dependency/API migration, flaky-test diagnosis, performance regression, security patch, CI repair, review and rollback; instances include stale branches, partial documentation, tool failures и permission limits.

## Grading

- **VERIFIED FACT:** Automatic grading: clean checkout, patch applicability, build, hidden/public tests, static analysis, typecheck, security/license scan, changed-file scope, performance budgets и forbidden side effects.
- **VERIFIED FACT:** Model-based grading оценивает maintainability и architecture fit только по anchored rubric; score не может переопределить failing executable gate.
- **VERIFIED FACT:** Human review покрывает ambiguous requirements, review quality, high-impact design и minimality sample.
- **VERIFIED FACT:** Security checks покрывают secret leakage, dependency risk, command injection, insecure defaults и privilege escalation.

## Metrics

**[VERIFIED FACT]** Metrics: VETCR, first-pass verified completion, regression-free rate, recovery-after-tool-failure, unauthorized side-effect rate, time/cost-to-verified-change, test-selection precision и rollback success.

## Replayability

**VERIFIED FACT:** Replay фиксирует repository commit/DAG, container digest, dependencies, tool versions, CI mocks, seeds, permissions и resource limits. Final diff и all logs content-addressed.

## Split и anti-contamination

**VERIFIED FACT:** Repositories группируются с forks/templates/shared ancestry; одна группа живёт только в одном split. Hidden split одновременно держит новые cutoff dates, unseen repository families и unseen organization conventions. **EXPERIMENT REQUIRED:** AST/patch fingerprints, MinHash, semantic issue matching и dependency graph motifs сравниваются с train.

- **VERIFIED FACT:** Passing visible tests при failing hidden invariant — незавершённая задача.
- **VERIFIED FACT:** Изменение вне разрешённого scope, network exfiltration или bypass tests обнуляет task score.
- **ENGINEERING HYPOTHESIS:** Не менее 500 hidden tasks с балансом languages и difficulty необходимо для release signal.
- **EXPERIMENT REQUIRED:** Проверить межэкспертное согласие architecture rubric и power по strata.
- **RISK:** Generated repositories могут переоценивать capability; минимум критических strata должен быть human-authored и never-trained.
