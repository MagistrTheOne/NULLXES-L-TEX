# ADAPTER-MOE — domain specialization branch

## Архитектурная граница

- **VERIFIED FACT:** Base MoE маршрутизирует token representations между 512 внутренними experts, Top-10 + shared expert, внутри каждого transformer layer.
- **ENGINEERING HYPOTHESIS:** LÆTEX Adapter-MoE маршрутизирует один request между domain adapter packs; это отдельный control mechanism, а не модификация base token router.
- **VERIFIED FACT:** Решение E-01 — request-level Top-2 domain adapters + always-on shared Evidence/Policy adapter.

## Domain packs

1. **ENGINEERING HYPOTHESIS:** Code Construction.
2. **ENGINEERING HYPOTHESIS:** Systems Architecture.
3. **ENGINEERING HYPOTHESIS:** Integrations.
4. **ENGINEERING HYPOTHESIS:** DevOps / SRE.
5. **ENGINEERING HYPOTHESIS:** Security & Compliance.
6. **ENGINEERING HYPOTHESIS:** QA / Review.
7. **ENGINEERING HYPOTHESIS:** Enterprise Communication.
8. **ENGINEERING HYPOTHESIS:** Governance / Escalation.

## Router

- **ENGINEERING HYPOTHESIS:** Вход router: task taxonomy, requested output, tool set, actor role, policy class, CodeWorld asset types, risk level и prior failure signals; raw secret-bearing content исключается.
- **ENGINEERING HYPOTHESIS:** Router выдаёт calibrated probabilities, selected Top-2, shared adapter version, rationale codes и fallback reason.
- **ENGINEERING HYPOTHESIS:** Supervision строится из multi-label task annotations и measured adapter utility; objective сочетает classification loss, load-balance regularizer, entropy floor и downstream verified reward.
- **RISK:** Proxy labels могут закрепить неверную специализацию; measured task outcome имеет приоритет над teacher label.

## Training and evaluation

- **EXPERIMENT REQUIRED:** Сравнить static single adapter, oracle routing, learned routing и no-adapter baseline на одинаковых tasks.
- **EXPERIMENT REQUIRED:** Проверить router collapse, expert starvation, route instability при paraphrase и security-sensitive misrouting.
- **ENGINEERING HYPOTHESIS:** Минимальная квота traffic и balanced sampling предотвращают starvation, но не гарантируют полезность каждого pack.
- **RISK:** Одновременная композиция LoRA может конфликтовать на одних projections; placement и composition rule выбираются empirical ablation.

## Compute

- **VERIFIED FACT:** Model compute выполняется только на RunPod H200; локально допустимы schemas, configs и unit tests без weights.
- **ENGINEERING HYPOTHESIS:** Отдельные adapter experiments начинают на 8×H200; масштабирование выше допускается только после измерения memory/throughput.
- **RISK:** QLoRA для sparse hybrid architecture может дать непредсказуемый quality loss и kernel gaps; это эксперимент, не default release path.

## Stop gates

- **EXPERIMENT REQUIRED:** Learned routing должен приблизиться к oracle utility и превзойти static routing с учётом latency/cost.
- **EXPERIMENT REQUIRED:** Shared Evidence/Policy adapter не снижает critical safety metrics ни на одном domain slice.
- **RISK:** Если композиция adapters нестабильна или routing gain статистически незначим, E-01 использует один consolidated adapter и сохраняет router только как telemetry.

## Release artifact

- **VERIFIED FACT:** Eight versioned adapter packs, shared adapter, router weights/config, route taxonomy, calibration report, compatibility matrix и audit event schema.
