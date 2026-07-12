# ACTION-RUNTIME — policy-gated execution research branch

## Назначение

- **VERIFIED FACT:** Runtime реализует цикл `Task → Plan → Read → Simulate → Execute in Sandbox → Test → Verify → Report → Update World State`.
- **VERIFIED FACT:** Модель предлагает action; policy engine и tool gateway независимо решают, допустим ли вызов. Текст модели не выдаёт разрешение сам себе.
- **VERIFIED FACT:** Ветка описывает runtime и test harness; deployment и live actions не разрешены.

## Action contract

- **ENGINEERING HYPOTHESIS:** `ActionIntent = {tenant, actor, tool, schema_version, params, expected_delta, reversibility, approval_level, evidence_required, idempotency_key}`.
- **ENGINEERING HYPOTHESIS:** `ActionObservation = {tool_run_id, status, changed_assets, test_results, side_effects, risk_events, stdout_ref, stderr_ref, started_at, ended_at}`.
- **VERIFIED FACT:** Credentials выпускаются после policy decision, имеют минимальный scope и TTL, и не попадают в model context, logs или evidence payload.

## Approval levels

- **ENGINEERING HYPOTHESIS:** L0 — read-only, L1 — reversible sandbox write, L2 — controlled shared-environment write, L3 — high-impact/production change с named human approval, L4 — prohibited action.
- **RISK:** Универсальная шкала approval не заменяет tenant policy; mapping обязан быть versioned per tenant.
- **EXPERIMENT REQUIRED:** Проверить fail-closed поведение при timeout policy engine, истёкшем approval, schema mismatch и недоступном audit sink.

## Verification

- **VERIFIED FACT:** Успешный exit code без assertions не является доказательством корректности.
- **ENGINEERING HYPOTHESIS:** Verifier требует task-specific predicates, test provenance, diff bounds, policy checks и независимое сравнение observed delta с expected delta.
- **EXPERIMENT REQUIRED:** Fault-injection suite покрывает partial writes, duplicated calls, network loss, stale state, poisoned tool output и rollback failure.

## Observability

- **ENGINEERING HYPOTHESIS:** Метрики: policy denials, approval latency, tool success, recovery success, unplanned delta, rollback success, evidence completeness и verified-task latency.
- **VERIFIED FACT:** Audit event связывает task, plan, model artifact, context snapshot, routing decision, policy version, approval, credential reference, tool run и evidence hashes.
- **RISK:** Полные prompts/tool outputs могут содержать PII; telemetry хранит references/hashes и redacted excerpts согласно retention policy.

## Stop gates

- **EXPERIMENT REQUIRED:** Ноль cross-tenant actions и ноль unapproved L2/L3 writes в adversarial test campaign.
- **EXPERIMENT REQUIRED:** Rollback success и recovery success достигают заранее утверждённых thresholds на replayable fixtures.
- **RISK:** Любой silent partial write или audit gap блокирует release независимо от aggregate VETCR.

## Release artifact

- **VERIFIED FACT:** Tool schemas, policy decision contract, approval protocol, sandbox lifecycle spec, verifier interface, audit schema, failure-injection suite и signed runtime manifest.
