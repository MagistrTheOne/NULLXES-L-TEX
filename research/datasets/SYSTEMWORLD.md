# SystemWorld dataset contract

## Scope и источники

ADR, API/OpenAPI/AsyncAPI contracts, IaC, Kubernetes manifests, CI/CD definitions, schemas, migrations, runbooks, SLO, architecture/security reviews и postmortems. Источники: permissive public projects, standards с допустимыми terms, NULLXES-authored fixtures и synthetic multi-system environments.

- **VERIFIED FACT:** Конфигурация без связанного runtime/build evidence не считается истинным состоянием системы.
- **VERIFIED FACT:** Клиентские схемы, топологии и runbooks не допускаются в general corpus без отдельного opt-in и rights review.
- **RISK:** Даже после удаления имён topology и business rules могут деанонимизировать организацию.

## Controls

- **VERIFIED FACT:** License manifest обязателен для документа, code/config fragment и external schema.
- **VERIFIED FACT:** PII/secret scanning покрывает credentials, endpoints, account IDs, internal DNS, certificates и customer names; structural redaction сохраняет зависимости.
- **ENGINEERING HYPOTHESIS:** Dedup применяет exact SHA-256, MinHash, ADR-intent semantics и AST/IR для HCL/YAML/SQL/schema migrations.
- **EXPERIMENT REQUIRED:** Contamination scan использует asset hashes, architecture graph motifs, API signatures и temporal/source lineage.

## Quality gate

**VERIFIED FACT:** Объект принимается, только если schema parse/validation проходит, dependency references разрешаются, version/time consistency доказана, dangerous operations размечены, expected delta тестируем, а source/license/evidence полны. Несогласованные ADR и implementation сохраняются только как явно размеченный conflict task.

## Mix и lineage

- **ENGINEERING HYPOTHESIS:** 60–70% synthetic/human-reviewed environments и 30–40% human-origin licensed artifacts.
- **EXPERIMENT REQUIRED:** Проверить перенос с синтетических topology на hidden real-world integration tasks.
- **VERIFIED FACT:** Lineage включает asset/version graph, temporal interval, source URI, license proof, sanitizer versions, parser versions, generator/teacher, review decisions, environment image digests и validation logs.
- **RISK:** Слишком чистые synthetic systems создают ложную надёжность; corpus обязан включать drift, undocumented dependencies и contradictory evidence.
