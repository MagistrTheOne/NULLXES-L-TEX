# ADAPTER-MOE PLANE

## Назначение

- **VERIFIED FACT:** Initial E-01 использует unified attention-only LoRA: retained `A1` identity/tool с отдельным BF16 merge `M1`, затем retained `A2` Action SFT с отдельным BF16 merge `M2`.
- **VERIFIED FACT:** Foundation имеет 160 внутренних experts, Top-8 и `shared_expert_intermediate_size: 0`; initial E-01 не LoRA-тюнингует все experts и не изменяет base router.
- **EXPERIMENT REQUIRED:** Восемь dynamic domain adapters и request-level Top-2 routing отложены до ablation после M2.

## Inputs / outputs

- **ENGINEERING HYPOTHESIS:** Inputs: authorized task metadata, tool inventory, asset classes, risk class, desired artifact и failure history.
- **VERIFIED FACT:** Initial output: один stage adapter ID/version и immutable lineage reference.
- **ENGINEERING HYPOTHESIS:** Deferred output: two domain adapter IDs/versions, внешний Evidence/Policy adapter, calibrated scores, rationale codes и fallback indicator.

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
- **EXPERIMENT REQUIRED:** Их полезность, attention placement, rank, composition order и per-domain data mix определяются ablation против unified adapter.
- **VERIFIED FACT:** Возможный внешний Evidence/Policy adapter не является shared expert base MoE.

## Staged train → verify → BF16 merge → train

- **VERIFIED FACT:** `S0 → A1 → M1`: train retained attention-only identity/tool LoRA `A1`, verify, затем отдельный BF16 merge `M1=S0+A1`.
- **VERIFIED FACT:** `M1 → A2 → M2`: train retained action-SFT adapter `A2` с fresh optimizer, verify, затем отдельный BF16 merge `M2=M1+A2`.
- **EXPERIMENT REQUIRED:** `A3 → M3 → A4 → M4` запускаются позднее и только от verified BF16 parent; FP8 создаётся отдельно от M4.
- **VERIFIED FACT:** FP8/INT4 parent, потеря adapter delta или mutable merge recipe являются hard stop.

## Failure modes

- **RISK:** Для deferred routing: router collapse, expert starvation, oscillating routes, incompatible composition, negative transfer, stale pack и Evidence/Policy suppression.
- **EXPERIMENT REQUIRED:** Oracle/static/learned/no-adapter comparison и paraphrase stability suite обязательны.

## Observability

- **ENGINEERING HYPOTHESIS:** Метрики: route distribution, entropy, calibration, per-pack utility, oracle regret, route latency, fallback rate, cross-domain error и critical safety rate.
- **VERIFIED FACT:** Audit хранит features by category, selected versions, scores и rationale codes; raw sensitive features не логируются.

## Release artifact

- **VERIFIED FACT:** Initial artifact: signed unified adapter, BF16 parent/merge hashes, merge recipe, eval report и rollback lineage.
- **EXPERIMENT REQUIRED:** Deferred artifact может добавить восемь packs, внешний Evidence/Policy adapter, router, taxonomy, calibration map и compatibility matrix.
