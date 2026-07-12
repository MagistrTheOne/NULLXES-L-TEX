# ADR-0004: запрет default training на raw tenant data

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Область: все LÆTEX datasets, training и telemetry.

## Контекст

- **RISK:** Enterprise repositories, tickets, logs и communications содержат proprietary code, PII, secrets, contractual restrictions и security topology.
- **VERIFIED FACT:** Operational access к tenant data не означает разрешение использовать их для общей модели.
- **RISK:** Простая деидентификация не устраняет memorization, membership inference и re-identification.

## Решение

- **VERIFIED FACT:** Raw tenant data по умолчанию запрещены в общем CPT, SFT, preference, RL, router и World Model training.
- **VERIFIED FACT:** Learning требует explicit opt-in с purpose, scope, data classes, retention, model lineage, revocation semantics и authorized approver.
- **VERIFIED FACT:** Tenant namespaces, encryption keys, object prefixes, lineage catalogs и processing jobs изолированы.
- **VERIFIED FACT:** Secret values удаляются до any training staging; данные с неясной лицензией/consent quarantined.

## Последствия

- **ENGINEERING HYPOTHESIS:** Общая модель обучается на licensed public, commissioned, synthetic и explicitly contributed datasets с provenance.
- **RISK:** Data flywheel растёт медленнее, но нарушение tenant trust является release-ending risk.
- **EXPERIMENT REQUIRED:** Privacy gates включают canary leakage, membership inference, memorization probes и cross-tenant retrieval tests.

## Opt-in artifact

- **VERIFIED FACT:** Каждая запись lineage содержит tenant, consent record, allowed purpose, transformations, source hash, PII/license scan, retention, dataset versions и derived checkpoints.
- **RISK:** Revocation после необратимого включения в weights технически сложна; договор и architecture должны ограничивать claims и поддерживать checkpoint lineage/retirement.
