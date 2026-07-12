# NULLXES LÆTEX

> Статус: source-of-truth scaffold  
> Дата фиксации источников: 2026-07-13

**VERIFIED FACT —** Компания: NULLXES. Developer / CEO: [@MagistrTheOne](https://github.com/MagistrTheOne). Контакты: [ceo@nullxes.com](mailto:ceo@nullxes.com), <https://nullxes.com>.

**ENGINEERING HYPOTHESIS —** LÆTEX — Enterprise Action Model: производная enterprise-модель, которая получает структурированное состояние организации, действует через контролируемые инструменты и возвращает проверяемый результат — изменение, тесты, evidence, риски и audit trail. В E-01 model workloads разворачиваются только в RunPod Secure Cloud на H200; on-prem/VPC клиента остаётся будущей product target и не заявляется как реализованный deployment.

**VERIFIED FACT —** Прямой foundation E-01 — [`Qwen/Qwen3-Coder-480B-A35B-Instruct`](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct): causal LM, прошедшая pretraining и post-training, 480B параметров всего / 35B активных, 62 слоя, hidden size 6144, GQA 96Q/8KV, head dimension 128, 160 routed experts, Top-8, без shared expert (`shared_expert_intermediate_size=0`), expert intermediate size 2560, vocabulary 151 936, native context 262 144 и BF16.

**VERIFIED FACT —** На дату проверки в официальных источниках не идентифицирован отдельно выпущенный `Qwen3-Coder-480B-A35B-Base`; upstream E-01 поэтому является Instruct checkpoint. Exact upstream SHA ещё не верифицирован и обозначается `PIN_BEFORE_TRAINING`, а не выдуманным revision.

**ENGINEERING HYPOTHESIS —** Broad CPT по умолчанию исключён: для уже post-trained Instruct checkpoint он создаёт высокий риск потери instruction/tool alignment. Допустимы только узкие, gated ablations после baseline evaluation.

**ENGINEERING HYPOTHESIS —** Lineage E-01: frozen BF16 S0 → identity/tool LoRA → verified BF16 merge M1 → enterprise Action SFT LoRA → merge M2 → preference optimization → GRPO → BF16 master M4 → FP8 serving derivative только после parity-проверки.

**ENGINEERING HYPOTHESIS —** Internal MoE router и experts на первых стадиях заморожены. Их adaptation разрешается только отдельным experiment gate после доказанного adapter ceiling.

**VERIFIED FACT —** `Qwen/Qwen3-Coder-Next-Base` 80B/3B больше не является foundation E-01. Он может упоминаться только как исторически отвергнутая или альтернативная ветвь.

**VERIFIED FACT —** Репозиторий описывает LÆTEX честно: это proprietary post-trained enterprise action model, built from open-weight foundations. Проект не заявляет pretraining from zero и не скрывает происхождение checkpoint в internal model card и юридических материалах.

**VERIFIED FACT —** Обучение и тяжёлый inference разрешены только на NVIDIA H200 в RunPod. Локальная машина — control/documentation plane без весов модели, датасетов клиента и training workloads.

**VERIFIED FACT —** Официальная card metadata для прямого upstream E-01 указывает Apache-2.0.

**RISK —** До загрузки весов, обучения и распространения derivative юридическая команда обязана закрепить exact revision, hashes, текст лицензии и notices. Metadata-tag без архивированного source manifest недостаточен.

## Границы текущего репозитория

**VERIFIED FACT —** Сейчас репозиторий является source-of-truth для архитектуры и источников, а не training stack и не runtime.

**ENGINEERING HYPOTHESIS —** Следующие реализации должны появляться только после утверждения контрактов: schemas состояния и действий, policy gates, dataset manifests, RunPod job specifications, evaluation harness и checkpoint registry.

**RISK —** Наличие документации не доказывает качество модели, безопасность исполнения, экономику H200 или превосходство над другими моделями. В репозитории нет и не заявляется ни одного verified benchmark result.

## Документы

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — границы системы, пять planes, closed loop, tenant isolation и артефакты.
- [`docs/SOURCES.md`](docs/SOURCES.md) — закреплённые официальные источники, revision checkpoint и журнал проверки.
- [`docs/RELEASE-GATES.md`](docs/RELEASE-GATES.md) — conjunctive hard gates и evidence contract.
- [`docs/ROADMAP-90D.md`](docs/ROADMAP-90D.md) — 13-недельный gated R&D roadmap.
- [`docs/SPEED-QUALITY.md`](docs/SPEED-QUALITY.md) — serving bakeoff, precision, cache isolation, экономика и latency targets.
- [`docs/RISK-REGISTER.md`](docs/RISK-REGISTER.md) — risks, triggers, mitigations и acceptance.
- [`docs/planes/`](docs/planes/) — Foundation, Adapter-MoE, CodeWorld, World Model и Execution/Verification.
- [`docs/branches/`](docs/branches/) — E-01 и условные research branches.
- [`docs/adr/`](docs/adr/) — зафиксированные архитектурные решения.
- [`research/identity/`](research/identity/) — identity overwrite contract и adversarial evaluation.
- [`research/datasets/`](research/datasets/) — LÆTEX Corpus contracts, lineage и tenant isolation.
- [`eval/laetex-bench/`](eval/laetex-bench/) — четыре evaluation tracks, metrics, anti-contamination и [`baseline manifest`](eval/laetex-bench/baseline-manifest.yaml).
- [`training/`](training/) — порядок фаз и phase-specific compute/gate contracts.
- [`infra/runpod/`](infra/runpod/) — H200-only compute architecture и семь документационных профилей.

## Жёсткие инварианты

1. **VERIFIED FACT —** На local control plane нет model weights, локального fine-tuning, CPT, RL, teacher generation или inference модели.
2. **ENGINEERING HYPOTHESIS —** Любое действие LÆTEX проходит policy check, исполняется в tenant-isolated sandbox и создаёт evidence.
3. **ENGINEERING HYPOTHESIS —** Клиентские данные по умолчанию не попадают в общий corpus; обучение возможно только по явному opt-in и отдельному договорному/техническому контуру.
4. **RISK —** RunPod availability, quota, topology и цена меняются; каждый запуск требует preflight-проверки конкретного H200-кластера, сети, storage и бюджета.
5. **EXPERIMENT REQUIRED —** Любое утверждение о latency, throughput, task completion, стоимости и качестве публикуется только после воспроизводимого прогона LÆTEX-Bench с закреплёнными artifacts.
