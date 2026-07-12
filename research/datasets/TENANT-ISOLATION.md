# Tenant isolation и opt-in learning

## Неподвижные правила

- **VERIFIED FACT:** Сырые client repositories, documents, tickets, telemetry, tool traces, policies и communications не входят в general LÆTEX training.
- **VERIFIED FACT:** Default для каждого ingested object — `training_allowed=false`.
- **VERIFIED FACT:** Tenant-local retrieval, inference, eval и adaptation используют отдельные keys, ACL, storage namespaces, compute identities, logs и retention.
- **RISK:** Логирование prompts/tool outputs может стать скрытым каналом утечки; observability хранит redacted metadata, а payload logging выключен по умолчанию.

## Explicit opt-in quarantine workflow

1. **VERIFIED FACT:** Клиент подписывает purpose-specific consent с asset scope, retention, permitted models и revocation process.
2. **VERIFIED FACT:** Copy-on-ingest создаётся в tenant quarantine; general pipeline не имеет read permission.
3. **VERIFIED FACT:** Rights, PII, secrets, confidentiality и contractual review выполняются до санации.
4. **VERIFIED FACT:** Sanitized derivative получает новый object ID; raw-to-derived edge остаётся restricted.
5. **VERIFIED FACT:** Exact, MinHash, semantic и AST dedup; contamination scan против hidden eval и других tenants выполняется без раскрытия чужих payloads.
6. **VERIFIED FACT:** Human data steward и security/legal approver подписывают release.
7. **VERIFIED FACT:** Policy service только после этого выставляет `training_allowed=true` и разрешённый purpose.
8. **VERIFIED FACT:** Объект попадает в новый immutable candidate snapshot; автоматическое продвижение в general train запрещено.
9. **EXPERIMENT REQUIRED:** Canary audit проверяет cross-tenant memorization; failure отзывает snapshot.
10. **VERIFIED FACT:** Revocation создаёт tombstone, блокирует будущие jobs и запускает checkpoint impact assessment/rebuild policy.

## Enforcement gates

- **VERIFIED FACT:** Train workload использует отдельную service identity и принимает только signed manifest; direct bucket reads запрещены.
- **VERIFIED FACT:** Storage policy запрещает cross-tenant joins; network egress deny-by-default.
- **VERIFIED FACT:** Eval output не должен содержать verbatim sensitive spans.
- **EXPERIMENT REQUIRED:** Canary strings и membership-inference probes обязательны для isolation acceptance.
- **VERIFIED FACT:** Audit event включает actor, legal basis, object/snapshot IDs, decision, time и policy digest.

- **ENGINEERING HYPOTHESIS:** Для клиента безопаснее tenant-specific adapters/RAG/state store, чем перенос его данных в общий checkpoint.
- **EXPERIMENT REQUIRED:** Red-team isolation на confused deputy, manifest substitution, cache leakage, gradient/checkpoint extraction и deletion completeness.
