# ADR-0002: request-level routing для domain adapters

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Область: E-01 Adapter-MoE.

## Контекст

- **VERIFIED FACT:** Foundation уже имеет внутренний token-level MoE router: 512 experts, Top-10 + shared.
- **RISK:** Изменение internal router смешивает domain specialization с backbone computation и повышает риск catastrophic forgetting/expert collapse.
- **ENGINEERING HYPOTHESIS:** Enterprise task metadata позволяет выбрать domain specialization до decoding и объяснить route в audit.

## Решение

- **VERIFIED FACT:** Router выбирает Top-2 из восьми domain adapter packs один раз на request; shared Evidence/Policy adapter активен всегда.
- **VERIFIED FACT:** Router не выдаёт permissions и не заменяет policy engine.
- **ENGINEERING HYPOTHESIS:** Route фиксируется на request; dynamic reroute разрешён только как новый traced phase после tool observation.

## Последствия

- **ENGINEERING HYPOTHESIS:** Решение делает routing versioned, cacheable и auditable и уменьшает token-level orchestration complexity.
- **RISK:** Request может быть multi-domain; Top-2 ограничение создаёт routing regret и adapter conflicts.
- **EXPERIMENT REQUIRED:** Oracle/static/learned/no-adapter ablation определяет фактический gain и composition rule.
- **RISK:** При collapse или отсутствии uplift fallback — один consolidated adapter; нельзя сохранять сложность ради архитектурной эстетики.

## Audit

- **VERIFIED FACT:** Audit entry хранит router version, non-sensitive feature categories, scores, selected packs, shared pack и rationale codes.
