# ADAPTER-MOE — domain specialization branch

## Архитектурная граница

- **VERIFIED FACT:** Base MoE маршрутизирует token representations между 160 внутренними experts, Top-8, без shared expert.
- **VERIFIED FACT:** Initial E-01 не изменяет base router и не применяет LoRA ко всем experts.
- **VERIFIED FACT:** Решение initial E-01 — unified attention-only adapters: M1 identity, затем M2 action SFT.
- **EXPERIMENT REQUIRED:** Request-level Top-2 из восьми domain adapters отложен; это будет отдельный control mechanism только при доказанном uplift.

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

- **EXPERIMENT REQUIRED:** Этот раздел описывает deferred experiment, а не принятую initial E-01 runtime architecture.
- **ENGINEERING HYPOTHESIS:** Вход router: task taxonomy, requested output, tool set, actor role, policy class, CodeWorld asset types, risk level и prior failure signals; raw secret-bearing content исключается.
- **ENGINEERING HYPOTHESIS:** Router выдаёт calibrated probabilities, selected Top-2, версию внешнего Evidence/Policy adapter, rationale codes и fallback reason.
- **ENGINEERING HYPOTHESIS:** Supervision строится из multi-label task annotations и measured adapter utility; objective сочетает classification loss, load-balance regularizer, entropy floor и downstream verified reward.
- **RISK:** Proxy labels от любого separately pinned future critic могут закрепить неверную специализацию; measured task outcome имеет приоритет.

## Training and evaluation

- **VERIFIED FACT:** Stage order: immutable BF16 S0 → attention-only identity LoRA M1 → hard verification → BF16 merge с retained adapter/hashes → fresh optimizer → action SFT M2.
- **VERIFIED FACT:** FP8/INT4 parent запрещён; preference M3 и GRPO M4 запускаются позднее только после M2 gates.
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
- **EXPERIMENT REQUIRED:** Внешний Evidence/Policy adapter не снижает critical safety metrics ни на одном domain slice и не должен смешиваться в терминологии с отсутствующим shared base expert.
- **RISK:** Если композиция adapters нестабильна или routing gain статистически незначим, E-01 использует один consolidated adapter и сохраняет router только как telemetry.

## Release artifact

- **VERIFIED FACT:** Initial artifact: versioned unified adapter, immutable BF16 parent/merged hashes, merge recipe, fresh-optimizer evidence и gate report.
- **EXPERIMENT REQUIRED:** Только successful deferred experiment добавляет eight packs, внешний Evidence/Policy adapter, router weights/config, route taxonomy и calibration report.
