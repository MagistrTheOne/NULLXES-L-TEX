# ADR-0002: request-level routing для domain adapters

- **VERIFIED FACT:** Статус: Accepted with staged deferral.
- **VERIFIED FACT:** Область: E-01 Adapter-MoE.

## Контекст

- **ENGINEERING HYPOTHESIS:** Independent E-01 target имеет внутренний token-level MoE router: 144 routed experts + 1 shared expert и Top-6; параметры остаются pending proxy validation по ADR-0007.
- **RISK:** Изменение internal router смешивает domain specialization с backbone computation и повышает риск catastrophic forgetting/expert collapse.
- **ENGINEERING HYPOTHESIS:** Enterprise task metadata позволяет выбрать domain specialization до decoding и объяснить route в audit.

## Решение

- **VERIFIED FACT:** Initial E-01 обучает unified attention-only stage adapters и не изменяет base router; LoRA всех 160 experts не входит в initial scope.
- **EXPERIMENT REQUIRED:** Dynamic request-level Top-2 routing восьми domain adapters отложен до доказанного uplift против unified-adapter control.
- **ENGINEERING HYPOTHESIS:** В будущем внешний Evidence/Policy adapter может быть always-on, но он не является и не называется shared base expert.
- **VERIFIED FACT:** Router не выдаёт permissions и не заменяет policy engine.
- **ENGINEERING HYPOTHESIS:** Route фиксируется на request; dynamic reroute разрешён только как новый traced phase после tool observation.

## Последствия

- **ENGINEERING HYPOTHESIS:** Решение делает routing versioned, cacheable и auditable и уменьшает token-level orchestration complexity.
- **RISK:** Request может быть multi-domain; Top-2 ограничение создаёт routing regret и adapter conflicts.
- **EXPERIMENT REQUIRED:** Oracle/static/learned/no-adapter ablation определяет фактический gain и composition rule.
- **RISK:** При collapse или отсутствии uplift fallback — один consolidated adapter; нельзя сохранять сложность ради архитектурной эстетики.

## Audit

- **VERIFIED FACT:** Initial audit хранит unified adapter/version и lineage stage.
- **EXPERIMENT REQUIRED:** Если dynamic routing будет принят, audit entry хранит router version, non-sensitive feature categories, scores, selected packs, внешний Evidence/Policy adapter и rationale codes.
