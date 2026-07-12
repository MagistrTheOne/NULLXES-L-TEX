# ADR-0005: heavy teacher используется только offline

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Область: E-01 teacher/quality tier.

## Контекст

- **VERIFIED FACT:** Canonical teacher candidate `Qwen/Qwen3-Coder-480B-A35B-Instruct` model card фиксирует 480B total, 35B activated, 62 layers, 160 experts, Top-8 и native 262 144 context.
- **RISK:** Постоянный teacher в live path увеличивает latency, стоимость, operational footprint и зависимость результата от отдельной модели.
- **RISK:** Teacher output не является ground truth и может передавать ошибки, identity и unsafe tool behavior.

## Решение

- **VERIFIED FACT:** Heavy teacher разрешён только offline для synthetic trajectories, candidate generation, critique, distillation и evaluation research на RunPod H200.
- **VERIFIED FACT:** Teacher не участвует в обычном live runtime, hard-case routing пользователя или approval decision.
- **VERIFIED FACT:** Никаких teacher generation runs не санкционировано данным ADR.

## Контроль качества

- **ENGINEERING HYPOTHESIS:** Teacher samples принимаются только после executable verifier, policy checks, provenance и human review для high-risk classes.
- **EXPERIMENT REQUIRED:** Сравнить teacher candidates и human/automatic verified outcomes; отбрасывать задачи, где verifier не может установить результат.
- **RISK:** Model-based judge того же семейства создаёт correlated bias; eval использует независимые graders и executable evidence.

## Последствия

- **VERIFIED FACT:** Runtime SLO и availability E-01 не зависят от teacher.
- **ENGINEERING HYPOTHESIS:** Offline amortization сохраняет quality benefit без live cost, если distillation реально улучшает frozen VETCR.
- **RISK:** Если uplift после verification статистически незначим, teacher budget прекращается.

## Release artifact

- **VERIFIED FACT:** Teacher manifest содержит exact repo/revision, tokenizer/config hashes, generation config, RunPod H200 topology, dataset lineage, verifier versions и accepted/rejected sample counts.
