# CODEWORLD-V0 — authoritative enterprise state substrate

## Цель

- **VERIFIED FACT:** CodeWorld V0 — не file RAG и не память prompt; это tenant-isolated graph + indexes + immutable event ledger, связывающие assets, versions, contracts, work items, evidence и policies.
- **ENGINEERING HYPOTHESIS:** Структурированное состояние уменьшит stale-context ошибки и объём prompt относительно recursive file stuffing.

## Scope

- **ENGINEERING HYPOTHESIS:** V0 индексирует repository tree, symbols, imports, dependency lockfiles, API contracts, Git refs, issues, CI, test artifacts, ADR, ownership, policy references и secret boundaries.
- **RISK:** Runtime telemetry включается только через агрегированные, access-filtered projections; сырые логи могут содержать secrets и PII.
- **VERIFIED FACT:** Secret values не индексируются. Хранятся классификация, location reference, owner и access policy.

## Data contracts

- **ENGINEERING HYPOTHESIS:** Узел: `{tenant_id, asset_id, type, version, content_hash, source_uri, classification, owner, observed_at}`.
- **ENGINEERING HYPOTHESIS:** Ребро: `{tenant_id, from, relation, to, source_event, confidence, valid_from, valid_to}`.
- **ENGINEERING HYPOTHESIS:** Evidence: `{evidence_id, producer, command/tool, inputs_hash, output_hash, result, timestamp, retention}`.
- **VERIFIED FACT:** Source connector остается authority для исходного объекта; CodeWorld authority — нормализованная snapshot/version связь и ledger наблюдений, но не внешняя business truth.

## Pipeline

1. **ENGINEERING HYPOTHESIS:** Connector пишет immutable source event с cursor/version.
2. **ENGINEERING HYPOTHESIS:** Parser строит typed nodes/edges и content-addressed artifacts.
3. **ENGINEERING HYPOTHESIS:** Reconciler помечает superseded версии, не перезаписывая историю.
4. **ENGINEERING HYPOTHESIS:** Policy projection удаляет недоступные actor-у узлы до retrieval.
5. **ENGINEERING HYPOTHESIS:** Context compiler передаёт модели минимальный evidence-backed slice с snapshot IDs.
6. **EXPERIMENT REQUIRED:** После action runtime выполняет targeted refresh затронутых assets и сверяет expected/observed delta.

## Exit criteria

- **EXPERIMENT REQUIRED:** Incremental update p95 и freshness SLO измерены отдельно по connector class.
- **EXPERIMENT REQUIRED:** Cross-tenant retrieval suite возвращает ноль чужих identifiers/content.
- **EXPERIMENT REQUIRED:** Любой context item трассируется до source URI, version и policy decision.
- **RISK:** Если graph maintenance не снижает VETCR errors или context cost на frozen tasks, расширение ontology останавливается.

## Release artifact

- **VERIFIED FACT:** Versioned ontology, connector contracts, event schemas, indexing jobs, policy projection API, context compiler и replay fixtures без tenant raw data.
