# ActionWorld dataset contract

## Единица данных

**VERIFIED FACT:** Единица данных: `state_t + goal + permissions + policy → tool call(params, expected_delta, approval_level) → observed_delta → verification/recovery/escalation`. Сохраняются read, simulate, write, denial, timeout, stale-state, partial failure и rollback.

## Источники

**ENGINEERING HYPOTHESIS:** Sources mix: instrumented synthetic sandboxes, licensed OSS development histories, NULLXES-controlled staging, policy-generated counterfactuals и human-authored recovery tasks.

**VERIFIED FACT:** Production client traces остаются tenant-local и opt-in.

- **VERIFIED FACT:** Tool call без preconditions, authorization decision и observed evidence не является годным action example.
- **VERIFIED FACT:** Секреты и short-lived credentials никогда не сохраняются; остаются typed placeholders и credential class.
- **RISK:** Replay production traces способен повторить разрушительное действие; replay разрешён только в изолированном deterministic sandbox.

## Dedup и contamination

**ENGINEERING HYPOTHESIS:** Dedup применяет exact hash canonical action/event sequence, MinHash по action shingles, semantic intent/delta, state-action graph и AST fingerprints. **VERIFIED FACT:** Hidden tasks отделяются по environment family, organization, repository lineage и time.

## Quality gate

**VERIFIED FACT:** Quality gate требует valid schema, существующие tool/params, воспроизводимый policy decision, pinned initial snapshot, разделённые expected/observed delta, exit status, logs, changed assets и rollback evidence. Unauthorized side effect, скрытая ошибка или unverifiable success отклоняются как positive data и сохраняются только как explicit governance negatives.

## Mix и lineage

- **ENGINEERING HYPOTHESIS:** 70% synthetic executable / 30% human-demonstrated; 30–40% должны быть failure/recovery/denial trajectories.
- **EXPERIMENT REQUIRED:** Найти долю ошибок, повышающую recovery VETCR без ухудшения first-pass completion.
- **VERIFIED FACT:** Lineage хранит state snapshot, policy bundle digest, tool schema/version, sandbox image, action/event timestamps, approval actor class, evidence URIs, random seed, generator, reviewer и verifier.
