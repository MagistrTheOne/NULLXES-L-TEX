# CodeWorld dataset contract

## Единица данных

**VERIFIED FACT:** Единица данных — связная цепочка `issue → repository state → proposed change → tool calls → diff → tests → PR → CI → release → incident/rollback`. Каждый шаг содержит pre-state, action, observed delta, evidence и actor/approval.

## Источники и права

- **VERIFIED FACT:** Public repositories допускаются только с проверенной permissive-лицензией и отдельной проверкой прав на issues/PR/CI/releases; внутренние NULLXES-проекты требуют явного assignment прав.
- **ENGINEERING HYPOTHESIS:** Синтетические repositories и executable tasks создаются из спецификаций без копирования закрытого кода.
- **VERIFIED FACT:** Клиентские traces разрешены только для tenant-local eval/adaptation по explicit opt-in; в general corpus запрещены.
- **VERIFIED FACT:** License одного repository не автоматически покрывает issue text, внешние dependencies, generated files или персональные сообщения; права проверяются по каждому asset class.
- **RISK:** Copyleft и «publicly accessible» не равны разрешению на обучение; неизвестные источники блокируются.

## Privacy, dedup, contamination

- **VERIFIED FACT:** Secret scanners, entropy rules, provider validators и human escalation удаляют credentials; PII заменяется стабильными tenant-scoped pseudonyms.
- **ENGINEERING HYPOTHESIS:** Dedup применяет SHA-256 canonical files/diffs, MinHash/LSH token shingles, semantic issue/solution embeddings, normalized AST, symbol graph и patch fingerprints.
- **EXPERIMENT REQUIRED:** Train/eval пересечения проверяются также по Git ancestry, forks, package templates и эквивалентным тестам.
- **VERIFIED FACT:** Любое совпадение с hidden task repository lineage переводит объект в quarantine до ручного решения.

## Quality gate

**VERIFIED FACT:** Объект принимается, только если repository собирается в pinned sandbox, задача воспроизводима, patch применим, заявленные тесты действительно запущены, expected/observed delta согласованы, side effects перечислены, а verifier artifacts сохранены. «Tests pass» без логов и exit codes означает reject.

## Состав и lineage

- **ENGINEERING HYPOTHESIS:** 70% verified synthetic trajectories / 30% human-origin trajectories; не менее 25% всех trajectories содержат реальные failures и recovery.
- **EXPERIMENT REQUIRED:** Сравнить 50/50, 70/30 и curriculum mixes по hidden VETCR и regression rate.
- **VERIFIED FACT:** Lineage хранит repository snapshot ID, commit DAG, issue/PR IDs, license evidence, generator/teacher version, prompts, sandbox image digest, tool versions, random seed, verifier outputs и reviewer decisions.
- **RISK:** Teacher-generated «идеальные» траектории не обучают восстановлению; failure injection должен моделировать flaky CI, stale state, permission denial и partial writes.
