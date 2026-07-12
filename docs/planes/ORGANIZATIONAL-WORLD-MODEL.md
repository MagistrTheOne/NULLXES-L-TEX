# ORGANIZATIONAL WORLD MODEL PLANE

## Formal contract

- **VERIFIED FACT:** `state_t = {assets, versions, goals, tasks, dependencies, permissions, policies, evidence, operational_signals}`.
- **VERIFIED FACT:** `action_t = {tool, params, expected_delta, approval_level}`.
- **VERIFIED FACT:** `observed_delta_t = {changed_assets, test_results, side_effects, risk_events, audit_entry}`.

## Inputs / outputs

- **ENGINEERING HYPOTHESIS:** Inputs: bounded CodeWorld snapshot, proposed action, policy snapshot, prior observations и evidence gaps.
- **ENGINEERING HYPOTHESIS:** Outputs: predicted typed delta, risk distribution, reversibility, missing evidence и recommendation `ask|plan|execute|escalate`.

## V0 / V1

- **VERIFIED FACT:** V0 — graph + immutable event ledger + deterministic policy engine; это state machine, не learned world model.
- **ENGINEERING HYPOTHESIS:** V1 — compact 1.5–3B learned transition model в shadow mode после накопления high-quality traces.
- **RISK:** Называть V0 «интеллектуальной моделью мира» без оговорки вводит в заблуждение.

## Trust boundary

- **VERIFIED FACT:** Predictions V1 не выдают permission, не меняют graph и не подтверждают tool success.
- **VERIFIED FACT:** Policy engine, approval service и observed tool delta находятся вне learned boundary.

## Authoritative state

- **VERIFIED FACT:** V0 event ledger + reconciled CodeWorld snapshot — authority; predicted state хранится отдельно с model/version/confidence.
- **VERIFIED FACT:** Только validated observations переводят predicted delta в observed delta.

## Tenant boundary

- **VERIFIED FACT:** State projections, traces, memory и learned tenant customization изолированы; общий V1 не использует raw tenant traces без explicit opt-in.
- **RISK:** Cross-tenant learned memorization возможна даже после removal identifiers; privacy evaluation обязательна.

## Durable memory

- **ENGINEERING HYPOTHESIS:** Durable memory хранит versioned facts/evidence и expiry rules, а не model summaries без provenance.
- **VERIFIED FACT:** Конфликт памяти разрешается source authority, version и observed_at; LLM не выбирает истину голосованием.

## Failure modes

- **RISK:** Hallucinated delta, overconfidence, policy drift, temporal leakage, causal misattribution, unobserved side effects и stale evidence.
- **EXPERIMENT REQUIRED:** Temporal, tenant-disjoint, OOD, counterfactual и abstention suites определяют readiness V1.

## Observability

- **ENGINEERING HYPOTHESIS:** Метрики: delta precision/recall, critical-risk recall, calibration error, abstention utility, false escalation, missing-evidence recall и V0 disagreement.
- **VERIFIED FACT:** Trace связывает state snapshot, action schema, prediction, confidence, policy decision, observation и final reconciliation.

## Release artifact

- **VERIFIED FACT:** V0 schemas/policy bundle/event ledger spec; отдельно для V1 — checkpoint reference, serialization schema, calibration artifact, shadow-mode report и lineage dossier.
