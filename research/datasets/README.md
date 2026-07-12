# LÆTEX Corpus: контракт программы данных

## Назначение

- **VERIFIED FACT:** LÆTEX Corpus разделён на CodeWorld, SystemWorld, Enterprise Voice, ActionWorld и GovernanceSet; объединение не отменяет отдельные лицензии, политики доступа и lineage.
- **VERIFIED FACT:** Сырые данные клиента запрещено включать в общий checkpoint, future-critic corpus, replay buffer или shared eval.
- **VERIFIED FACT:** Для любого объекта по умолчанию `training_allowed=false`; отсутствие поля трактуется как запрет.
- **ENGINEERING HYPOTHESIS:** Первая полезная версия корпуса требует 65–75% проверенных синтетических объектов и 25–35% человеческих/open-source объектов; доля пересматривается после ablation.
- **EXPERIMENT REQUIRED:** Доказать, что синтетика повышает VETCR на hidden-наборах, а не только имитирует стиль generator/critic.

## Единый pipeline допуска

**VERIFIED FACT:** `ingest → quarantine → classify → license/consent → PII/secret scan → normalize → exact dedup → MinHash dedup → semantic/AST dedup → contamination scan → quality gate → immutable snapshot`

**VERIFIED FACT:** Обязательные состояния: `quarantined`, `rejected`, `eval_only`, `training_candidate`, `approved_snapshot`. Только объект с `training_allowed=true`, валидным `consent_record_id`, пройденными gates и записью в manifest может попасть в train snapshot.

## Общие gates

1. **VERIFIED FACT:** License gate блокирует неизвестную, несовместимую или непроверяемую лицензию.
2. **VERIFIED FACT:** Privacy gate блокирует PII, credentials, secrets, private keys и tenant identifiers до доказанной санации.
3. **VERIFIED FACT:** Dedup gate применяет SHA-256 к canonical form, MinHash/LSH к near-duplicates, embeddings к смысловым дублям; для кода дополнительно AST/token fingerprints.
4. **VERIFIED FACT:** Contamination gate сравнивает train с hidden eval по exact hash, MinHash, semantic similarity, symbol/AST fingerprints и provenance graph.
5. **VERIFIED FACT:** Quality gate требует schema validity, разрешённый source, reproducible verifier, evidence и отсутствие несанкционированных side effects.
6. **RISK:** Semantic dedup может удалить легитимные независимые решения или пропустить перефразированную утечку; thresholds версионируются и калибруются на размеченной выборке.

## Хранение и управление

- **VERIFIED FACT:** Immutable encrypted object storage хранит raw quarantine, sanitized canonical objects, manifests и verifier artifacts.
- **VERIFIED FACT:** Metadata/lineage store хранит source, hashes, license, consent, transformations, tenant, split, reviewers и toolchain versions.
- **VERIFIED FACT:** KMS keys, ACL и retention разделены по tenant и purpose; train workers читают только approved immutable snapshots.
- **VERIFIED FACT:** Snapshot имеет content-addressed ID; изменение любого объекта создаёт новый snapshot.
- **VERIFIED FACT:** Удаление по отзыву consent выполняется через tombstone, impact graph и rebuild затронутых snapshots/checkpoints.

## Первичные targets

- **ENGINEERING HYPOTHESIS:** Broad CPT отсутствует в E-01; узкий DAPT отключён по умолчанию.
- **EXPERIMENT REQUIRED:** Corpus size для опционального narrow DAPT остаётся `TBD_BY_PILOT` и фиксируется только после отдельного S0-based pilot с contamination, alignment, coding-retention, tool-grammar и cost gates.
- **ENGINEERING HYPOTHESIS:** SFT: 180k–300k verified examples.
- **ENGINEERING HYPOTHESIS:** Executable trajectories: 60k–120k.
- **ENGINEERING HYPOTHESIS:** Failure/recovery trajectories: 20k–60k.
- **ENGINEERING HYPOTHESIS:** Private held-out evaluation: 2,000–3,000 задач.
- **EXPERIMENT REQUIRED:** Зафиксировать targets только после Phase-0 power analysis, leakage audit и стоимости верификации.

**VERIFIED FACT:** Схема объектов определена в [LINEAGE-SCHEMA.md](LINEAGE-SCHEMA.md), а клиентская изоляция — в [TENANT-ISOLATION.md](TENANT-ISOLATION.md).
