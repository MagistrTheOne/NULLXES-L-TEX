# ADR-0005: foundation не является teacher; future critic только offline

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Область: E-01 foundation и future critic/quality tier.

## Контекст

- **VERIFIED FACT:** `Qwen/Qwen3-Coder-480B-A35B-Instruct` — direct post-trained foundation E-01: 480B total, 35B activated, 62 layers, 160 experts, Top-8 и native 262 144 context.
- **VERIFIED FACT:** Foundation не считается teacher для собственного post-training и не используется как доказательство качества собственных synthetic labels.
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
