# ADR-0005: external teacher/critic только offline

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Область: external critic/quality tier; уточнён ADR-0009.

## Контекст

- **VERIFIED FACT:** По ADR-0007 E-01 является independent from-scratch model без внешнего weight parent.
- **VERIFIED FACT:** Qwen не является foundation; ADR-0009 допускает его только как benchmark и опциональный offline synthetic teacher.
- **RISK:** Выход любого будущего critic/teacher не является ground truth и может передавать correlated errors, identity и unsafe tool behavior.

## Решение

- **EXPERIMENT REQUIRED:** Любой future critic/teacher выбирается отдельным сравнением, получает exact pinned repo/revision/config/tokenizer и работает только offline на H200.
- **VERIFIED FACT:** Future critic/teacher не участвует в обычном live runtime, hard-case routing пользователя или approval decision.
- **VERIFIED FACT:** Никаких critic/teacher generation runs и никакого конкретного critic checkpoint данным ADR не санкционировано.

## Контроль качества

- **ENGINEERING HYPOTHESIS:** Critic samples принимаются только после executable verifier, policy checks, provenance и human review для high-risk classes.
- **EXPERIMENT REQUIRED:** Сравнить отдельно pinned critic candidates и human/automatic verified outcomes; отбрасывать задачи, где verifier не может установить результат.
- **RISK:** Model-based judge того же семейства создаёт correlated bias; eval использует независимые graders и executable evidence.

## Последствия

- **VERIFIED FACT:** Runtime SLO и availability E-01 не зависят от critic/teacher.
- **ENGINEERING HYPOTHESIS:** Offline critic может быть полезен только если distillation реально улучшает frozen VETCR.
- **RISK:** Если uplift после verification статистически незначим, critic budget прекращается.

## Release artifact

- **VERIFIED FACT:** Critic manifest содержит exact repo/revision, tokenizer/config hashes, generation config, H200 topology, dataset lineage, verifier versions и accepted/rejected sample counts.

## Relation

- **VERIFIED FACT:** При конфликте с этим документом ADR-0009 имеет приоритет.
