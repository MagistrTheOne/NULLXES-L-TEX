# LÆTEX-2 — независимая foundation research target

## Решение

- **ENGINEERING HYPOTHESIS:** LÆTEX-2 исследуется только после доказанного product/data flywheel E-01; это не обещание release.
- **VERIFIED FACT:** Исправленная арифметическая гипотеза использует 62, а не 64 слоя для согласования порядка 159B total / 14B active.
- **RISK:** Грубая parameter arithmetic не доказывает trainability, quality, throughput или оптимальность архитектуры.

## Corrected 62-layer hypothesis

| Параметр | Значение |
|---|---|
| Layers | **ENGINEERING HYPOTHESIS:** 62 |
| Hidden size | **ENGINEERING HYPOTHESIS:** 6144 |
| Attention | **ENGINEERING HYPOTHESIS:** GQA 48Q/8KV, head dim 128 |
| Experts | **ENGINEERING HYPOTHESIS:** 64 routed + 1 shared per layer |
| Routing | **ENGINEERING HYPOTHESIS:** Top-2 routed + shared |
| Expert FFN | **ENGINEERING HYPOTHESIS:** SwiGLU, intermediate 2048 |
| Vocabulary | **ENGINEERING HYPOTHESIS:** 151 936, untied input/output embeddings |
| Context | **ENGINEERING HYPOTHESIS:** hybrid attention, staged 32K→128K→256K+ |

## Parameter arithmetic

- **ENGINEERING HYPOTHESIS:** Один expert содержит приблизительно `3 × 6144 × 2048 = 37.75M` weights.
- **ENGINEERING HYPOTHESIS:** Routed experts дают `62 × 64 × 37.75M ≈ 149.8B`; shared experts — `62 × 37.75M ≈ 2.34B`.
- **ENGINEERING HYPOTHESIS:** Один full-attention block при 48Q/8KV и head dim 128 содержит около `88.1M`; верхняя оценка для 62 blocks — `≈5.46B`.
- **ENGINEERING HYPOTHESIS:** Untied embeddings дают `2 × 151936 × 6144 ≈ 1.87B`.
- **ENGINEERING HYPOTHESIS:** С norms/router и без точной DeltaNet parameterization итог порядка `159.5B total`.
- **ENGINEERING HYPOTHESIS:** Active path Top-2+shared: `62 × (3 × 37.75M + 88.1M) + 1.87B ≈ 14.35B`; hybrid blocks изменят точное число.
- **RISK:** FFN intermediate 2048 равен d/3 и может ограничить expert capacity; высокий total parameter count не компенсирует слабый per-expert representation.

## Research program

- **EXPERIMENT REQUIRED:** Проверить dense/MoE scaling на 1B, 7B и 20–30B proxy models с одинаковой data curriculum; уменьшение здесь — research proxy, не замена target release model.
- **EXPERIMENT REQUIRED:** Сравнить 64×2048 Top-2+shared с 32×4096 Top-2+shared и менее sparse alternative при сопоставимом active compute.
- **ENGINEERING HYPOTHESIS:** Training budget требует нескольких триллионов deduplicated, licensed tokens; точный token target выводится из proxy scaling laws, а не назначается декларативно.
- **RISK:** 159B sparse model с 14B active может быть data-, routing- или communication-limited; EP all-to-all может уничтожить theoretical efficiency.

## Infrastructure assumptions

- **VERIFIED FACT:** Разрешены только однородные RunPod NVIDIA H200 workloads; локальные model workloads и другие классы accelerator запрещены.
- **EXPERIMENT REQUIRED:** До каждого multi-node run конкретный allocation обязан подтвердить NVLink/NVSwitch intra-node topology, provider-attested InfiniBand/high-bandwidth inter-node fabric и NCCL collective acceptance. Внешняя документация RunPod не аттестует выделенный cluster.
- **RISK:** Allocation без fabric attestation, isolated object storage, tracked runs и checkpoint registry не допускается к LÆTEX-2 research run независимо от заявленного GPU SKU.
- **ENGINEERING HYPOTHESIS:** Stack: Megatron-Core/DeepSpeed-class runtime с TP, PP, EP, DP, sequence/context parallelism и distributed optimizer.
- **ENGINEERING HYPOTHESIS:** Минимальный meaningful large-scale systems prototype — 64×H200; target pretraining capacity вероятно требует сотен H200 и подтверждённой multi-node efficiency.
- **RISK:** Ни GPU count, ни wall-clock нельзя честно зафиксировать без token budget, achieved MFU, sequence mix, optimizer state format и RunPod topology benchmark.
- **VERIFIED FACT:** Локальный control plane хранит только configs, redacted metadata и telemetry; weights/train workloads локально запрещены.

## Stop gates

1. **EXPERIMENT REQUIRED:** E-01 не доказывает устойчивый VETCR/product advantage и proprietary data flywheel — stop.
2. **EXPERIMENT REQUIRED:** Proxy scaling не превосходит dense/less-sparse alternatives на quality per active FLOP — stop.
3. **EXPERIMENT REQUIRED:** Router load balance, expert specialization и recovery после expert/node faults не проходят gates — stop.
4. **EXPERIMENT REQUIRED:** H200 cluster не достигает заранее утверждённых MFU/network efficiency и checkpoint-resume SLO — stop.
5. **EXPERIMENT REQUIRED:** Licensed corpus и provenance не покрывают утверждённый token budget — stop.
6. **RISK:** Если минимальная команда меньше примерно 18–30 специалистов по model, data, distributed systems, eval, security и infra либо timeline меньше 24–36 месяцев, программа нереалистична; диапазон требует staffing validation.

## Release artifact

- **VERIFIED FACT:** До прохождения stop gates разрешены только architecture spec, parameter calculator, proxy experiment reports, data readiness report и compute feasibility dossier; foundation checkpoint не обещан.
