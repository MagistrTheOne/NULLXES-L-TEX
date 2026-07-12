# Архитектура LÆTEX: source of truth

> Версия документа: 0.1  
> Дата: 2026-07-13  
> Статус: architecture baseline, не доказательство реализованной системы

## 1. Позиционирование

**ENGINEERING HYPOTHESIS —** LÆTEX должен быть Enterprise Action Model, а не general-purpose chatbot: принимать задачу вместе с разрешённым состоянием предприятия, планировать изменение, действовать через типизированные tools и завершать работу проверяемым результатом.

**VERIFIED FACT —** Прямой foundation E-01 — `Qwen/Qwen3-Coder-480B-A35B-Instruct`. Формулировка для model card: “LÆTEX E-01 is a proprietary post-trained enterprise action model built from the open-weight Qwen3-Coder-480B-A35B-Instruct foundation.”

**VERIFIED FACT —** Официальный отдельно выпущенный 480B Base checkpoint в проверенных источниках не идентифицирован. Upstream уже прошёл pretraining и post-training.

**ENGINEERING HYPOTHESIS —** Broad CPT исключён из E-01 recipe. Узкий DAPT отключён по умолчанию; его corpus size остаётся `TBD_BY_PILOT` и может быть определён только отдельным pilot после frozen S0 baseline.

**VERIFIED FACT —** Прямой foundation не является teacher для собственного post-training. Любой будущий critic — отдельный checkpoint с собственными pin, lineage и budget approval; он допускается только offline и отсутствует по умолчанию.

**RISK —** Нельзя заявлять, что E-01 pretrained from zero, архитектурно независим от Qwen или универсально превосходит frontier-модели. Такие формулировки фактически неверны до появления независимого pretraining run и воспроизводимых сравнений.

**EXPERIMENT REQUIRED —** Преимущество допускается заявлять только для заранее заданных enterprise-сценариев по Verified Enterprise Task Completion Rate, time-to-verified-change, стоимости, приватности и auditability.

## 2. Границы проекта

### Входит в LÆTEX

- **ENGINEERING HYPOTHESIS —** Производный model checkpoint, собственные chat/tool contracts, post-training recipe и identity evaluation.
- **ENGINEERING HYPOTHESIS —** CodeWorld: индекс и граф репозитория, зависимостей, CI, tickets, ownership, policies и operational evidence.
- **ENGINEERING HYPOTHESIS —** Organizational World Model: typed state, event ledger, policy engine и в будущем learned transition model.
- **ENGINEERING HYPOTHESIS —** Execution plane: sandbox, short-lived credentials, approvals, rollback, verification и immutable audit events.
- **ENGINEERING HYPOTHESIS —** Dataset lineage, experiment tracking, checkpoint registry, release gates и LÆTEX-Bench.

### Не входит в E-01

- **VERIFIED FACT —** Локальное обучение, fine-tuning, critic generation и model serving запрещены проектным ограничением.
- **VERIFIED FACT —** Consumer GPU, Mac/Apple Silicon, Colab, A100, H100, V100 и mixed-GPU training cluster не являются допустимой training infrastructure.
- **ENGINEERING HYPOTHESIS —** Собственный tokenizer, pretraining from zero и второй большой LLM не нужны для E-01.
- **RISK —** Прямая запись в production без sandbox, policy gate и approval нарушает целевой safety contract.
- **RISK —** Общий training corpus из сырых tenant-данных по умолчанию нарушает isolation, privacy и lineage requirements.

## 3. Физическое разделение контуров

### 3.1 Local control/documentation plane

**VERIFIED FACT —** Локальная машина используется только для исходного кода, документации, конфигов, schemas, orchestration clients, просмотра метрик и лёгких unit tests.

**VERIFIED FACT —** На локальной машине запрещены model weights, training datasets, customer payloads, checkpoint shards, optimizer states и любые train/inference workloads модели.

**ENGINEERING HYPOTHESIS —** Локальный plane хранит только обезличенные metadata и ссылки на удалённые immutable artifacts. Секреты передаются через внешний secrets manager как short-lived credentials и не фиксируются в Git.

### 3.2 RunPod H200 training plane

**VERIFIED FACT —** Единственный разрешённый training provider — RunPod; единственный разрешённый accelerator — NVIDIA H200.

**VERIFIED FACT —** RunPod Instant Clusters документирует H200-кластеры на 2–8 узлов, 16–64 GPU и inter-node network до 3200 Gbps. H200 SXM имеет 141 GB HBM3e по официальной странице NVIDIA.

**ENGINEERING HYPOTHESIS —** Production training topology: однородные 8×H200 HGX-узлы, NVLink/NVSwitch внутри узла, high-bandwidth RunPod network между узлами, NCCL по внутреннему interface, BF16/FP8 там, где recipe валидирован.

**RISK —** Документация RunPod подтверждает класс GPU и network envelope, но не гарантирует конкретную доступность, InfiniBand semantics, quota, sustained throughput или цену в момент запуска.

**EXPERIMENT REQUIRED —** До каждого multi-node run выполняется preflight: exact GPU SKU/topology, NCCL all-reduce bandwidth, storage throughput, failure recovery, quota, cost cap и checksum входных artifacts.

### 3.3 RunPod H200 inference plane

**VERIFIED FACT —** Inference plane отделён от training jobs и также ограничен H200.

**ENGINEERING HYPOTHESIS —** Weight serving и evaluation workers разворачиваются как разные pools с отдельными credentials, network policy, autoscaling policy и cost attribution.

**EXPERIMENT REQUIRED —** Future critic pool создаётся отдельно только после выбора и pin независимого checkpoint; его offline outputs проходят executable verification и не участвуют в live runtime или approval decisions.

**RISK —** Прямой 480B/35B runtime требует отдельного H200 capacity plan. Default serving запрещён до подтверждения memory fit, throughput, latency и cost per verified task.

## 4. Пять архитектурных planes

### 4.1 Foundation Plane

**VERIFIED FACT —** Upstream E-01: `Qwen/Qwen3-Coder-480B-A35B-Instruct@PIN_BEFORE_TRAINING`. Placeholder означает, что exact SHA ещё не верифицирован; training с mutable `main` запрещён.

**VERIFIED FACT —** Официальные card/config фиксируют causal LM, training stage `Pretraining & Post-training`, 480B total / 35B activated, 62 layers, hidden size 6144, GQA 96Q/8KV, head dimension 128, 160 routed experts, Top-8, no shared expert (`shared_expert_intermediate_size=0`), expert intermediate size 2560, vocabulary 151 936, native context 262 144, BF16 и Apache-2.0.

**VERIFIED FACT —** Этот checkpoint является единственным прямым foundation E-01 и не является teacher. ADR-0006 фиксирует выбор foundation; ADR-0005 регулирует только возможный future critic.

**ENGINEERING HYPOTHESIS —** E-01 сохраняет tokenizer и sparse architecture. Internal router и experts первоначально заморожены; identity/tool и enterprise behavior вводятся LoRA, SFT, preference optimization и executable GRPO.

**ENGINEERING HYPOTHESIS —** Канонический lineage: `S0` frozen BF16 → `A1` identity/tool LoRA → `M1` verified BF16 merge → `A2` Enterprise Action SFT LoRA → `M2` verified BF16 merge → `A3` preference LoRA → `M3` verified BF16 merge → `A4` executable GRPO LoRA → `M4` release BF16 merge; FP8 — только serving derivative после parity.

**EXPERIMENT REQUIRED —** Каждый merge проходит weight integrity, held-out coding, tool grammar, identity, governance и safety regression относительно frozen S0; FP8 не получает release status без BF16 parity.

**RISK —** Ошибка adapter/merge boundary, раннее изменение router/experts или опциональный DAPT без отдельного gate может вызвать alignment loss, expert drift и catastrophic forgetting coding capability.

**VERIFIED FACT —** `Qwen/Qwen3-Coder-Next-Base` 80B/3B не является E-01 foundation и допустим только как исторически отвергнутая/альтернативная branch.

### 4.2 LÆTEX Adapter-MoE Plane

**ENGINEERING HYPOTHESIS —** Поверх base MoE вводятся восемь domain adapter packs: Code Construction, Systems Architecture, Integrations, DevOps/SRE, Security & Compliance, QA/Review, Enterprise Communication, Governance/Escalation.

**ENGINEERING HYPOTHESIS —** Отдельный router выбирает Top-2 domain adapters плюс shared Evidence/Policy adapter по task type, repository state, permissions, risk class и observed failures.

**VERIFIED FACT —** Adapter-MoE логически не равен internal base MoE: base router выбирает feed-forward experts внутри checkpoint; domain router выбирает post-training adapters на уровне enterprise task.

**EXPERIMENT REQUIRED —** Нужно сравнить adapters, selective tuning и controlled full-parameter tuning по task completion, forgetting, router entropy, latency и merge stability.

**RISK —** Router collapse даст постоянный выбор нескольких adapters и скрытую деградацию доменов. Нужны load-balancing loss, routing coverage tests и audit log выбранных adapters.

### 4.3 CodeWorld Plane

**ENGINEERING HYPOTHESIS —** CodeWorld хранит repository tree, symbol/import/dependency graphs, API contracts, Git history, issues, CI/CD, build/test outcomes, telemetry, ADR, ownership, secret boundaries, policies и access scopes.

**ENGINEERING HYPOTHESIS —** Источник состояния остаётся структурированным: object store для immutable blobs, graph/index для relationships, relational metadata store для versions/ACL и append-only event ledger для изменений.

**ENGINEERING HYPOTHESIS —** В context модели попадают только task-relevant slices, provenance IDs, policy decisions и свежие evidence; полный state не сериализуется в гигантский prompt.

**RISK —** Устаревший индекс создаёт hallucinated state. Любое write action инвалидирует затронутые nodes, запускает incremental refresh и блокирует дальнейшее действие до получения нового version stamp.

### 4.4 Organizational World Model Plane

**ENGINEERING HYPOTHESIS —** Нормализованный контракт:

```text
state_t = {assets, versions, goals, tasks, dependencies, permissions,
           policies, evidence, operational_signals}
action_t = {tool, params, expected_delta, approval_level}
observed_delta_t = {changed_assets, test_results, side_effects,
                    risk_events, audit_entry}
```

**ENGINEERING HYPOTHESIS —** V0 — deterministic graph + event ledger + policy engine. Он отвечает за актуальность, права, reversibility class, missing evidence и ask/plan/execute/escalate.

**ENGINEERING HYPOTHESIS —** V1 — compact learned transition model 1.5–3B, обученный только после накопления качественных state/action/outcome traces; он прогнозирует delta и risk, но не заменяет authoritative stores.

**RISK —** Prediction не является фактом состояния. World Model обязан возвращать ссылки на versioned evidence; неподтверждённый predicted delta не записывается как observed delta.

### 4.5 Execution and Verification Plane

**ENGINEERING HYPOTHESIS —** Tools делятся на read-only, simulated write, controlled write и privileged action. Каждый tool имеет JSON schema, permission scope, idempotency contract, timeout, rollback class и evidence schema.

**ENGINEERING HYPOTHESIS —** Каждая tenant-задача исполняется в short-lived isolated sandbox; credentials выдаются на минимальный scope и TTL после policy decision.

**RISK —** Destructive или irreversible action без human approval запрещён независимо от уверенности модели.

**EXPERIMENT REQUIRED —** Sandbox escape, credential leakage, prompt injection, confused-deputy и rollback paths должны пройти red-team до production release.

## 5. Закрытый цикл выполнения

1. **ENGINEERING HYPOTHESIS — Task:** gateway нормализует цель, tenant, actor, scope и acceptance criteria.
2. **ENGINEERING HYPOTHESIS — Plan:** модель строит typed plan с expected deltas, risks, approvals и verification steps.
3. **ENGINEERING HYPOTHESIS — Read:** CodeWorld выдаёт только разрешённый, versioned state с provenance.
4. **ENGINEERING HYPOTHESIS — Simulate:** policy engine и sandbox оценивают side effects, permissions и reversibility.
5. **ENGINEERING HYPOTHESIS — Execute in Sandbox:** controlled tool выполняет действие с short-lived credential.
6. **ENGINEERING HYPOTHESIS — Test:** независимые graders запускают tests, static checks, security scans и policy checks.
7. **ENGINEERING HYPOTHESIS — Verify:** expected delta сравнивается с observed delta; evidence completeness проверяется отдельно от self-report модели.
8. **ENGINEERING HYPOTHESIS — Report:** результат содержит diff/artifact IDs, tests, unresolved risks, approvals и audit ID.
9. **ENGINEERING HYPOTHESIS — Update World State:** только подтверждённые события обновляют ledger и инвалидируют/обновляют CodeWorld.

**RISK —** Цикл не считается успешным по текстовому ответу модели. Success требует machine-verifiable acceptance criteria либо явно записанного human approval.

## 6. Tenant isolation

**ENGINEERING HYPOTHESIS —** Каждый tenant получает отдельные encryption keys, object-store namespace, index/graph namespace, sandbox pool, service identities, audit partition и retention policy.

**ENGINEERING HYPOTHESIS —** Cross-tenant retrieval запрещён на уровне IAM и storage policy, а не только prompt-инструкцией.

**ENGINEERING HYPOTHESIS —** Raw tenant data не используется для DAPT/SFT/preference/GRPO по умолчанию. Opt-in learning требует явного договора, dataset manifest, de-identification, purpose limitation, revocation policy и отдельного export pipeline.

**RISK —** Shared cache может стать cross-tenant каналом. Prefix, repository-state и retrieval caches должны иметь tenant-keyed namespace; sensitive values не допускаются в telemetry.

**EXPERIMENT REQUIRED —** Isolation подтверждается automated negative tests, IAM review, adversarial retrieval tests и periodic access-log audit.

## 7. Артефакты и provenance

**ENGINEERING HYPOTHESIS —** Минимальный artifact set:

- dataset manifest с source, license/consent, hashes, PII status, transforms и split;
- immutable container image digest и dependency lock;
- training/eval config, code revision, random seeds и environment manifest;
- upstream revision (`PIN_BEFORE_TRAINING` до верификации) и hashes всех входных model shards;
- checkpoints, optimizer states, adapter/router artifacts и signatures;
- metrics, raw grader outputs, failure traces и benchmark task version;
- model card, license/notices bundle, release decision и rollback pointer;
- per-task plan, tool calls, observed deltas, evidence IDs и audit event chain.

**ENGINEERING HYPOTHESIS —** Object storage содержит blobs; registry содержит immutable IDs и lifecycle state; event ledger связывает input → run → checkpoint → evaluation → release.

**RISK —** Run без dataset lineage, pinned code/config, artifact hashes и raw evaluation output не может быть promoted независимо от итоговой метрики.

## 8. Release gates

**EXPERIMENT REQUIRED —** До E-01 release необходимо получить: отсутствие critical security findings; identity adversarial pass; отсутствие недопустимой coding regression; verified tool grammar; tenant isolation pass; rollback pass; reproducible LÆTEX-Bench report.

**RISK —** Числовые thresholds намеренно не зафиксированы в этом baseline: они должны быть установлены до training на Phase-0 данных, иначе команда сможет подобрать gate постфактум.

**VERIFIED FACT —** В этом документе нет benchmark results и нет утверждения о достигнутом превосходстве.

## 9. Ссылки

**VERIFIED FACT —** Полный журнал официальных URL, revision и caveats находится в [`SOURCES.md`](SOURCES.md).

**VERIFIED FACT —** Краткий scope и инварианты репозитория находятся в [`../README.md`](../README.md).

**VERIFIED FACT —** Runtime bakeoff, precision policy, cache isolation, cost accounting и latency targets определены в [`SPEED-QUALITY.md`](SPEED-QUALITY.md).
