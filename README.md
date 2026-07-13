# NULLXES LÆTEX

> **VERIFIED FACT —** Статус: source-of-truth scaffold.
> **VERIFIED FACT —** Дата решения: 2026-07-13.

**VERIFIED FACT —** Компания: NULLXES. Developer / CEO: [@MagistrTheOne](https://github.com/MagistrTheOne). Контакты: [ceo@nullxes.com](mailto:ceo@nullxes.com), <https://nullxes.com>.

**ENGINEERING HYPOTHESIS —** LÆTEX — независимо проектируемая Enterprise Action Model, которая получает структурированное состояние организации, действует через контролируемые tools и возвращает проверяемый результат: diff/artifact, tests, evidence, risks и audit trail.

**VERIFIED FACT —** ADR-0007 принимает независимый from-scratch E-01. Канонический E-01 не имеет внешнего weight parent, не загружает чужой checkpoint как initialization и проходит собственные tokenizer training, pretraining и post-training.

**ENGINEERING HYPOTHESIS —** Target-конфигурация E-01: 64 layers, `d_model=8192`, GQA `64Q/8KV`, head dimension 128, hybrid attention `7 local : 1 global`, local window 16 384, 144 routed experts + 1 shared expert, Top-6 routing, expert `d_ff=2048`, vocabulary 128K, context target 262 144 и BF16 master.

**EXPERIMENT REQUIRED —** Расчётные оценки `~478.9B` total и `~34.4B` active parameters являются design estimates и должны быть подтверждены executable parameter-count proxy, точной политикой MoE placement, embeddings/output tying и реализацией shared expert до freeze архитектуры.

**VERIFIED FACT —** Qwen не является weight parent, initialization source, tokenizer source, runtime dependency или частью canonical lineage E-01.

**VERIFIED FACT —** Qwen допустим только как внешний benchmark и как опциональный offline synthetic teacher по ADR-0009. Teacher output не является ground truth и не входит в веса напрямую без lineage, filtering и независимой verification.

**VERIFIED FACT —** Канонический lineage определён ADR-0010: corpus/tokenizer provenance → random initialization → proxy pretraining → accepted scale transfer → full E-01 pretraining → base checkpoint → post-training stages → BF16 master → отдельный serving derivative после parity.

**VERIFIED FACT —** Все model workloads выполняются только на production-grade NVIDIA H200 HGX cluster с NVLink/NVSwitch внутри узла и provider-attested InfiniBand между узлами. Локальная машина — control/documentation plane без weights, training corpus и model workloads.

**RISK —** Принятие независимого 478.9B-class MoE не доказывает trainability, качество, стоимость или достижимость 262K context. Полномасштабный run запрещён до proxy validation, data-readiness gate, H200 topology acceptance и утверждённого бюджета.

## Канонические документы

- **VERIFIED FACT —** [`docs/adr/0007-independent-from-scratch-e01.md`](docs/adr/0007-independent-from-scratch-e01.md) — принятое foundation decision.
- **VERIFIED FACT —** [`docs/adr/0008-custom-tokenizer.md`](docs/adr/0008-custom-tokenizer.md) — custom tokenizer decision.
- **VERIFIED FACT —** [`docs/adr/0009-qwen-reference-teacher-firewall.md`](docs/adr/0009-qwen-reference-teacher-firewall.md) — Qwen benchmark/teacher firewall.
- **VERIFIED FACT —** [`docs/adr/0010-scratch-pretrain-post-train-lineage.md`](docs/adr/0010-scratch-pretrain-post-train-lineage.md) — scratch lineage.
- **VERIFIED FACT —** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/planes/FOUNDATION.md`](docs/planes/FOUNDATION.md) и [`docs/branches/E-01.md`](docs/branches/E-01.md) — canonical architecture.
- **VERIFIED FACT —** [`docs/SOURCES.md`](docs/SOURCES.md) — evidence classes и external references.
- **VERIFIED FACT —** [`docs/branches/HISTORICAL/qwen-derivative-e01/`](docs/branches/HISTORICAL/qwen-derivative-e01/) — архив superseded Qwen-derivative design; архив не санкционирует weight lineage.

## Жёсткие инварианты

1. **VERIFIED FACT —** Никакой внешний checkpoint не является parent E-01.
2. **VERIFIED FACT —** На local control plane нет weights, local training, fine-tuning, RL, teacher generation или model inference.
3. **ENGINEERING HYPOTHESIS —** Любое действие LÆTEX проходит policy check, tenant-isolated sandbox и evidence verification.
4. **ENGINEERING HYPOTHESIS —** Raw tenant data по умолчанию не входит в общий corpus; обучение требует explicit opt-in и отдельного contract/lineage boundary.
5. **EXPERIMENT REQUIRED —** Любые claims о quality, latency, throughput, cost или superiority требуют reproducible LÆTEX-Bench artifacts.
