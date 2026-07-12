# CODEWORLD PLANE

## Назначение

- **VERIFIED FACT:** CodeWorld — structured operational substrate, а не RAG по файлам.
- **ENGINEERING HYPOTHESIS:** Он объединяет repository tree, symbols, imports/dependencies, API contracts, Git, tickets, CI/CD, tests, telemetry projections, ADR, ownership, secret boundaries, policies и scopes.

## Inputs / outputs

- **ENGINEERING HYPOTHESIS:** Inputs: versioned connector events, repository snapshots, build/test artifacts, policy metadata и action observations.
- **ENGINEERING HYPOTHESIS:** Outputs: policy-filtered state slice, graph queries, freshness metadata, evidence references и post-action reconciliation delta.

## Trust boundary

- **VERIFIED FACT:** Connectors аутентифицируются per tenant; parser output считается untrusted до schema validation, malware/content controls и source reconciliation.
- **VERIFIED FACT:** Context compiler применяет access policy до retrieval, а не фильтрует уже собранный prompt.

## Authoritative state

- **VERIFIED FACT:** External systems остаются source authorities; CodeWorld ledger авторитетен для того, что и когда было observed/indexed.
- **VERIFIED FACT:** Каждый fact имеет source URI, version/hash, observed_at и confidence; без них он не попадает в model context.

## Tenant boundary

- **VERIFIED FACT:** Separate namespaces, encryption keys, indexes, object prefixes, queues, caches и retention policies.
- **RISK:** Ошибка tenant predicate в graph/vector query критична; enforcement дублируется storage policy и application authorization.

## Storage and retrieval

- **ENGINEERING HYPOTHESIS:** Property graph хранит typed relations; object storage — immutable content/evidence; relational store — cursors/policies/transactions; search index — lexical/symbol lookup.
- **ENGINEERING HYPOTHESIS:** Retrieval сначала выбирает structured candidates и versions, затем извлекает минимальные source spans; raw long context используется только для bounded, evidenced artifacts.
- **EXPERIMENT REQUIRED:** Сравнить graph-first, lexical-only и long-context stuffing по VETCR, stale-fact rate, token cost и latency.

## Incremental refresh

- **ENGINEERING HYPOTHESIS:** Event cursors + content hashes ограничивают re-indexing изменёнными assets; dependency closure пересчитывается bounded breadth.
- **VERIFIED FACT:** После каждого write action targeted refresh обязателен до final report; mismatch expected/observed delta создаёт risk event.

## Failure modes

- **RISK:** Stale snapshot, split-brain connectors, dangling edges, parser poisoning, hidden generated files, secret ingestion, policy drift и cross-tenant leakage.
- **EXPERIMENT REQUIRED:** Replay, stale-state, connector reorder и adversarial repository suites входят в release gate.

## Observability

- **ENGINEERING HYPOTHESIS:** Метрики: freshness lag, parse coverage, provenance completeness, retrieval precision/recall, context tokens, policy denials, reconciliation mismatch и tenant-isolation violations.
- **VERIFIED FACT:** Query trace связывает actor, policy version, graph snapshot, candidates, selected spans и model task.

## Release artifact

- **VERIFIED FACT:** Versioned ontology, connector SDK contracts, schemas, graph migrations, indexer/context compiler, policy filters, reconciliation service spec и replay fixtures.
