# ADAPTER-MOE PLANE

## Назначение

- **ENGINEERING HYPOTHESIS:** Plane специализирует E-01 через восемь domain packs, request-level Top-2 routing и always-on shared Evidence/Policy adapter.
- **VERIFIED FACT:** Это routing adapters на уровне request, а не 512-expert token routing внутреннего base MoE.

## Inputs / outputs

- **ENGINEERING HYPOTHESIS:** Inputs: authorized task metadata, tool inventory, asset classes, risk class, desired artifact и failure history.
- **ENGINEERING HYPOTHESIS:** Outputs: two adapter IDs/versions, shared adapter version, calibrated scores, rationale codes и fallback indicator.

## Trust boundary

- **VERIFIED FACT:** Router не видит secret values и не принимает approval decisions.
- **RISK:** Manipulated task metadata может направить запрос в слабый domain pack; policy enforcement остаётся downstream и независимым.

## Authoritative state

- **VERIFIED FACT:** Adapter registry и signed compatibility manifest авторитетны для доступных packs; router output — recommendation для model orchestrator.
- **VERIFIED FACT:** Routing rationale не доказывает correctness действия.

## Tenant boundary

- **VERIFIED FACT:** Общие adapters не обучаются на raw tenant data по умолчанию; tenant-specific packs физически/логически изолированы и не смешиваются в batch/cache.
- **RISK:** Adapter names и selection telemetry могут раскрывать task category; audit access ограничивается tenant.

## Domain packs

- **ENGINEERING HYPOTHESIS:** Code Construction; Systems Architecture; Integrations; DevOps/SRE; Security & Compliance; QA/Review; Enterprise Communication; Governance/Escalation.
- **EXPERIMENT REQUIRED:** Placement, rank, composition order и per-domain data mix определяются ablation, а не единым rank для всех layers.

## Failure modes

- **RISK:** Router collapse, expert starvation, oscillating routes, incompatible adapter composition, negative transfer, stale pack и policy adapter suppression.
- **EXPERIMENT REQUIRED:** Oracle/static/learned/no-adapter comparison и paraphrase stability suite обязательны.

## Observability

- **ENGINEERING HYPOTHESIS:** Метрики: route distribution, entropy, calibration, per-pack utility, oracle regret, route latency, fallback rate, cross-domain error и critical safety rate.
- **VERIFIED FACT:** Audit хранит features by category, selected versions, scores и rationale codes; raw sensitive features не логируются.

## Release artifact

- **VERIFIED FACT:** Signed adapter packs, shared adapter, router artifact, taxonomy, calibration map, compatibility matrix, eval report и routing audit schema.
