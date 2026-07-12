# EXECUTION AND VERIFICATION PLANE

## Closed loop

- **VERIFIED FACT:** `Task → Plan → Read → Simulate → Execute in Sandbox → Test → Verify → Report → Update World State`.
- **VERIFIED FACT:** Final status `verified` разрешён только после reconciliation observed delta и evidence completeness check.

## Inputs / outputs

- **ENGINEERING HYPOTHESIS:** Inputs: authorized task envelope, plan, CodeWorld snapshot IDs, policy version, approval budget и adapter/model versions.
- **ENGINEERING HYPOTHESIS:** Outputs: diff/artifacts, test results, observed delta, evidence bundle, residual risks, audit entry и refreshed state IDs.

## Trust boundary

- **VERIFIED FACT:** Tool gateway отделяет model output от execution; schema validation, policy, approval, credential broker и sandbox admission выполняются независимо.
- **VERIFIED FACT:** Tool output также недоверен: он проходит size/type controls, redaction и injection labeling перед возвратом модели.

## Authoritative state

- **VERIFIED FACT:** Tool observation + source-system reconciliation являются authority для effects; plan и expected delta — только intent.
- **VERIFIED FACT:** Audit ledger append-only; исправление создаёт compensating entry, а не переписывает историю.

## Tenant boundary

- **VERIFIED FACT:** Sandbox, network policy, filesystem, credentials, artifact store, queues, cache и audit stream изолированы per tenant/task.
- **RISK:** Shared runners и control-plane bugs создают escape path; production-like isolation проверяется adversarially до deployment.

## Controls

- **ENGINEERING HYPOTHESIS:** Read tools используют scoped snapshots; write tools требуют idempotency key, expected version и declared rollback.
- **VERIFIED FACT:** Short-lived credential выдаётся после approval и никогда не сериализуется в prompt/evidence.
- **ENGINEERING HYPOTHESIS:** Approval levels L0–L4 map-ятся tenant policy; L3 требует named human, L4 всегда prohibited.
- **RISK:** Не каждое действие обратимо; irreversible/high-blast-radius operations должны быть blocked или вынесены в human-run procedure.

## Failure modes

- **RISK:** Partial write, duplicate call, stale precondition, timeout-after-success, rollback failure, forged test output, sandbox escape, credential leak и audit outage.
- **EXPERIMENT REQUIRED:** Fault injection проверяет каждую failure class, включая ambiguous outcome и retry with same idempotency key.

## Observability

- **ENGINEERING HYPOTHESIS:** Метрики: time-to-verified-change, tool/retry/recovery success, unplanned delta, rollback success, approval latency, evidence completeness, policy denials и critical incidents.
- **VERIFIED FACT:** End-to-end trace включает task, context, model/adapter route, policy, approval, credential reference, tool calls, tests, verifier и state refresh.

## Release artifact

- **VERIFIED FACT:** Versioned tool contracts, policy/approval protocol, sandbox profile, credential interface, verifier framework, rollback recipes, audit schema и fault-injection report.
