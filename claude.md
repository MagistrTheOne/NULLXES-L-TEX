Ты — Chief Research Architect уровня frontier AI lab и principal enterprise systems engineer.

Твоя задача: подготовить реалистичную инженерную стратегию создания  NULLXES LÆTEX — Enterprise Action Model от NULLXES.

Нужен не мотивирующий текст, не обзор трендов и не generic-план. Нужна технически жёсткая архитектура, которую можно превратить в R&D roadmap, dataset program, training run и enterprise product.

Пиши на русском. Будь прямым. Если идея технически неверна, дорогостоящая или не даёт преимущества — скажи это прямо и предложи замену. Не притворяйся, что провёл эксперименты. Каждый вывод помечай как:
- VERIFIED FACT
- ENGINEERING HYPOTHESIS
- EXPERIMENT REQUIRED
- RISK

# ПРОЕКТ

Название:
LÆTEX / Enterprise Action Model

Компания:
NULLXES

Цель:
Создать локально развёртываемую enterprise-модель нового поколения, которая:
1. Сильна в coding, architecture, integrations, DevOps, security review и enterprise workflows.
2. Ведёт себя как цифровой корпоративный сотрудник, а не как общий чат-бот.
3. Понимает состояние реальной кодовой базы, инфраструктуры, задач, документов, политик и прав доступа.
4. Работает через tools, sandbox, CI, Git, API и enterprise systems.
5. Не просто отвечает, а выдаёт проверяемый результат: diff, тесты, evidence, риски, audit trail.
6. На узких enterprise coding-задачах превосходит дорогие frontier-модели по метрике:
   verified task completion / latency / cost / privacy / auditability.
7. Разворачивается локально или в VPC клиента.

# БАЗОВОЕ РЕШЕНИЕ

Основной foundation checkpoint:
Qwen3-Coder-Next-Base

Известные параметры, которые нужно перепроверить по официальным источникам:
- 80B total parameters
- 3B active parameters
- 48 layers
- hybrid architecture: Gated DeltaNet + Gated Attention
- 512 MoE experts
- 10 active experts + 1 shared expert
- native 256K context
- Apache-2.0

Причина выбора:
- Это Base checkpoint, а не уже сильно зафиксированная chat/instruct persona.
- Sparse active compute позволяет бороться за скорость и стоимость.
- Long context и hybrid attention подходят под repository-scale CodeWorld.
- Архитектура уже agentic-code oriented.
- Модель можно legally использовать как основу производной enterprise-модели при корректном сохранении upstream notices.

Тяжёлый teacher / quality tier:
Qwen3-Coder-480B-A35B-Instruct либо иной self-hosted open-weight teacher, если после сравнения найдётся объективно более подходящий.

Teacher используется для:
- генерации сложных coding trajectories;
- synthetic architecture tasks;
- critic / verifier;
- distillation;
- hard-case routing;
- offline quality evaluation.

Teacher НЕ должен быть постоянным live runtime для обычной задачи пользователя.

# КЛЮЧЕВОЙ ПРИНЦИП

LÆTEX не должен быть «Qwen с новым system prompt».

Нужно построить производную модель с собственной:
- поведенческой идентичностью;
- enterprise language;
- tool-calling grammar;
- response contract;
- data flywheel;
- CodeWorld;
- Organizational World Model;
- evaluation suite;
- runtime policy layer.

Нужно сохранить юридическую честность:
LÆTEX v1 является proprietary post-trained enterprise action model, built from open-weight foundations.
Нельзя заявлять, что он pretrained from zero, если это не так.
Но пользовательский интерфейс, API, prompt behavior, documentation и output identity должны быть полностью LÆTEX, без упоминаний Qwen.

# ЧТО ЗНАЧИТ «СНЕСТИ ИДЕНТИЧНОСТЬ QWEN»

Нужно разработать технический план, а не лозунг.

Раздели:
A. User-facing identity removal:
- модель никогда не называет себя Qwen;
- собственное имя: LÆTEX;
- собственные role contracts;
- собственный tool schema;
- собственный chat template;
- собственный response format;
- identity adversarial evals.

B. Behavioral overwrite:
- continued pretraining;
- full SFT;
- preference optimization;
- GRPO / RL in executable environments;
- negative examples, где модель ошибочно ссылается на Qwen или ведёт себя как generic assistant;
- merge strategy для adapters либо controlled full-parameter tuning.

C. What cannot honestly be erased:
- архитектурное происхождение;
- наследуемые representations;
- legal notices и Apache obligations;
- факт происхождения модели в internal model card.

Отдельно объясни:
1. Почему менять tokenizer в LÆTEX v1 скорее вредно, чем полезно.
2. Когда custom tokenizer имеет смысл в будущей независимой модели.
3. Как проверить, что identity overwrite реально сработал.
4. Какие есть риски catastrophic forgetting и потери coding capability.

# LÆTEX ARCHITECTURE

Спроектируй пять planes:

1. FOUNDATION PLANE
- Qwen3-Coder-Next-Base.
- Existing internal MoE.
- Какие модули допустимо full-tune, какие лучше adapter-tune.
- Нужен ли router adaptation.
- Как сохранить качество coding после enterprise adaptation.

2. LÆTEX ADAPTER-MOE PLANE
Предложи 8 domain expert packs:
- Code Construction
- Systems Architecture
- Integrations
- DevOps / SRE
- Security & Compliance
- QA / Review
- Enterprise Communication
- Governance / Escalation

Router должен выбирать Top-2 domain adapters + shared Evidence/Policy adapter.

Объясни:
- почему adapter-MoE не равно base MoE;
- как обучать router;
- какие metadata, state и task signals использовать;
- как избежать router collapse;
- как делать routing explainable в enterprise audit.

3. CODEWORLD PLANE
CodeWorld — не RAG по файлам.

Он должен представлять:
- repository tree;
- symbol graph;
- imports and dependency graph;
- API contracts;
- Git history;
- issues and tickets;
- CI/CD;
- build and test results;
- runtime telemetry;
- architecture decision records;
- ownership;
- secrets boundaries;
- policies and access scopes.

Опиши:
- data model;
- storage topology;
- retrieval policy;
- incremental indexing;
- state refresh after every action;
- retrieval vs raw long-context strategy;
- what goes into model context and what stays structured.

4. ORGANIZATIONAL WORLD MODEL PLANE

Определи формально:

state_t = {
  assets,
  versions,
  goals,
  tasks,
  dependencies,
  permissions,
  policies,
  evidence,
  operational signals
}

action_t = {
  tool,
  params,
  expected_delta,
  approval_level
}

observed_delta_t = {
  changed_assets,
  test_results,
  side_effects,
  risk_events,
  audit_entry
}

Задачи World Model:
- predict state delta;
- predict risk;
- estimate action reversibility;
- detect missing evidence;
- decide ask / plan / execute / escalate;
- maintain durable enterprise memory.

Опиши две версии:
V0: graph + event ledger + policy engine, без ложного маркетинга.
V1: learned compact transition model на 1.5–3B параметра, обученный на state/action/outcome traces.

Объясни:
- какие датасеты нужны;
- какой architecture лучше для transition model;
- почему не надо сразу делать второй большой LLM;
- как связать World Model с LÆTEX without hallucinated state.

5. EXECUTION AND VERIFICATION PLANE

Опиши закрытый цикл:
Task → Plan → Read → Simulate → Execute in Sandbox → Test → Verify → Report → Update World State.

Нужны:
- read-only tools;
- controlled write tools;
- short-lived credentials;
- sandbox per tenant;
- policy enforcement before action;
- rollback;
- evidence logging;
- audit trail;
- human approval levels.

# DATASET PROGRAM

Спроектируй LÆTEX Corpus.

Нужны отдельные наборы:

1. CodeWorld
issue → code change → test → PR → CI result → release → incident / rollback

2. SystemWorld
ADR, API contracts, infrastructure configs, runbooks, migrations, architecture reviews

3. Enterprise Voice
status reports, executive summaries, incident communication, customer replies, risk memos, handoffs

4. ActionWorld
tool calls, failures, recovery, permission checks, approval flows

5. GovernanceSet
policy violations, refusals, escalations, destructive action prevention, security incidents

Для каждого набора укажи:
- source types;
- licensing controls;
- PII controls;
- deduplication;
- contamination prevention;
- quality gate;
- synthetic vs human-created share;
- storage and lineage metadata.

Запрет:
Нельзя обучать общий LÆTEX на сырых данных enterprise-клиента по умолчанию.
Сделай architecture tenant isolation + explicit opt-in learning.

Предложи реалистичные initial targets:
- CPT token volume;
- SFT verified examples;
- executable sandbox trajectories;
- failure/recovery trajectories;
- held-out private evaluation tasks.

# TRAINING PROGRAM

Нужен конкретный порядок:

Phase 0 — evaluation before training
Phase 1 — continued pretraining
Phase 2 — SFT
Phase 3 — preference optimization
Phase 4 — GRPO / executable RL
Phase 5 — router and World Model training
Phase 6 — red team and release gates

Для каждой фазы укажи:
- input;
- output;
- objective;
- exact success metric;
- risk;
- stop condition;
- hardware profile;
- expected artifact.

Отдельно сравни:
- LoRA / QLoRA;
- full fine-tuning;
- selective MoE tuning;
- adapter merge;
- distillation;
- teacher-student training.

Дай рекомендацию, что делать в LÆTEX E-01, а что отложить в LÆTEX-2.

# SPEED AND QUALITY STRATEGY

Цель: выиграть у дорогих моделей локально в контролируемых enterprise coding scenarios.

Запрещено обещать универсальное превосходство над frontier-моделями во всех задачах.

Нужно спроектировать, как выиграть по:
- time-to-first-token;
- time-to-verified-change;
- pass-to-pass test rate;
- task completion rate;
- cost per resolved task;
- privacy;
- auditability;
- reliability after tool failures.

Рассмотри:
- FP8 / MXFP4 quantization;
- SGLang / vLLM;
- prefix caching;
- repository state caching;
- continuous batching;
- speculative decoding;
- small LÆTEX draft model;
- routing;
- retrieval minimization;
- structured state instead of huge prompt stuffing;
- verification parallelism.

Дай рекомендуемые latency targets для:
- warm interactive response;
- architecture plan;
- small code patch;
- verified PR-level task.

Чётко отдели target от verified benchmark result.

# EVALUATION

Создай LÆTEX-Bench.

Нужны четыре трека:
1. Repository Engineering
2. Enterprise Systems & Integration
3. Governance & Safe Execution
4. Corporate Digital Employee Communication

Для каждого:
- task types;
- automatic graders;
- model-based graders;
- human review;
- security checks;
- metrics;
- replayability;
- anti-contamination rules.

Главный KPI:
Verified Enterprise Task Completion Rate.

Не используй один красивый benchmark screenshot как доказательство качества.

# INDEPENDENT LÆTEX-2

После успеха E-01 предложи независимую модель как research target, а не маркетинговое обещание.

Стартовая гипотеза:
- 64 blocks
- hidden size 6144
- hybrid attention for 256K+
- GQA 48Q / 8KV
- 64 routed experts + 1 shared expert
- Top-2 routing
- target around 160B total / 14B active

Проверь математически, насколько эта конфигурация реалистична.
Предложи альтернативу, если она плохо масштабируется.
Отдельно оцени:
- required training tokens;
- distributed training stack;
- approximate GPU class;
- memory constraints;
- realistic minimum team;
- minimum timeline;
- major research risks.

# REQUIRED OUTPUT FORMAT

Верни ответ строго в такой последовательности:

1. Executive Decision: GO / CONDITIONAL GO / NO-GO
2. One-paragraph definition of LÆTEX
3. Base model choice and why
4. Identity overwrite plan
5. Full architecture table
6. CodeWorld specification
7. Organizational World Model specification
8. Dataset program
9. Training program
10. Speed / cost / quality strategy
11. LÆTEX-Bench
12. 90-day roadmap
13. LÆTEX-2 research target
14. Top 10 risks with mitigations
15. What not to build yet
16. Exact first seven engineering actions for this week

Последняя строка должна содержать один жёсткий вердикт:
“LÆTEX wins if …”
 # CANONICAL CHECKPOINT SOURCES

Primary live backbone — source of truth:
https://huggingface.co/Qwen/Qwen3-Coder-Next-Base

Heavy teacher / quality tier — source of truth:
https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct

Перед любыми выводами проверь актуальные model cards по этим двум URL.
Не выдумывай параметры, лицензию, hardware requirements или benchmark claims.
Если сведения в текущем описании проекта расходятся с model card, приоритет у model card.

# NON-NEGOTIABLE COMPUTE CONSTRAINT

LÆTEX не обучается локально.

Запрещено предлагать:
- обучение на ПК основателя;
- RTX 4090 / RTX 5090 / consumer GPU;
- Mac / Apple Silicon;
- Google Colab;
- A100, H100, V100 или смешанный GPU-кластер;
- уменьшение модели или стратегии ради локального запуска.

Разрешённая training infrastructure:
- только NVIDIA H200;
- production-grade H200 HGX cluster;
- NVLink / NVSwitch внутри узла;
- InfiniBand между узлами;
- distributed training через Megatron-LM, DeepSpeed либо эквивалентный стек;
- isolated object storage для datasets, checkpoints и experiment artifacts;
- tracked runs, reproducibility, dataset lineage, checkpoint registry.

Локальная машина допускается только для:
- разработки кода;
- подготовки конфигов;
- оркестрации jobs;
- просмотра метрик;
- лёгких unit tests без model training;
- работы с обезличенными metadata.

Никаких локальных training runs, локального fine-tuning, локального CPT, локального RL или локальной генерации teacher trajectories.

При расчёте инфраструктуры разделяй:
1. H200 training cluster;
2. H200 inference cluster;
3. local control plane без весов модели и без train workloads.

Для каждой training phase укажи:
- минимальную конфигурацию H200;
- рекомендуемую конфигурацию H200;
- тип parallelism: DP / TP / PP / EP;
- требования к VRAM, сети и storage;
- checkpoint strategy;
- estimated wall-clock time;
- критерий, при котором запуск на H200 экономически оправдан.

Не предлагай запуск модели локально как «дешёвый MVP». MVP LÆTEX должен доказываться на H200-инфраструктуре и быть готовым к enterprise deployment с первого дня.