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

**VERIFIED FACT —** ADR-0007 принимает independent from-scratch E-01 без external weight parent, checkpoint initialization или inherited tokenizer.

**ENGINEERING HYPOTHESIS —** Canonical target: 64 layers, `d_model=8192`, GQA `64Q/8KV`, head dimension 128, hybrid attention `7 local : 1 global`, local window 16 384, 144 routed experts + 1 shared expert, Top-6, expert `d_ff=2048`, vocabulary 128K, context target 262 144 и BF16 master.

**EXPERIMENT REQUIRED —** `~478.9B total / ~34.4B active` — provisional design estimates pending executable parameter-count proxy, MoE placement and exact shared/embedding accounting.

**VERIFIED FACT —** Canonical lineage: corpus/tokenizer provenance → random initialization → proxies → signed scale gate → full pretraining → BF16 base → SFT → preference → executable RL → BF16 master → parity-gated serving derivative.

**VERIFIED FACT —** Qwen не является weight parent, tokenizer source или runtime dependency. Он допустим только как benchmark и optional offline synthetic teacher за firewall ADR-0009.

**RISK —** Независимый 478.9B-class pretraining имеет критические data, convergence, H200 communication, recovery, schedule и economic risks; full-scale run запрещён до proxy/data/systems/budget gates.

# КЛЮЧЕВОЙ ПРИНЦИП

LÆTEX не должен быть rebrand или derivative внешнего checkpoint.

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
**VERIFIED FACT —** E-01 заявляется from scratch только если artifact graph подтверждает собственный tokenizer, random initialization, pretraining и post-training без external weight parent.
**RISK —** Architectural ideas, external teacher data и benchmark references должны иметь provenance; from-scratch weights не означают отсутствие third-party data/license obligations.

# ЧТО ЗНАЧИТ НЕЗАВИСИМАЯ IDENTITY

Нужно разработать технический план, а не лозунг.

Раздели:
A. User-facing identity:
- модель идентифицирует себя как LÆTEX;
- собственное имя: LÆTEX;
- собственные role contracts;
- собственный tool schema;
- собственный chat template;
- собственный response format;
- identity adversarial evals.

B. Behavioral post-training:
- **ENGINEERING HYPOTHESIS —** enterprise Action SFT;
- **ENGINEERING HYPOTHESIS —** preference optimization;
- **ENGINEERING HYPOTHESIS —** GRPO / RL in executable environments;
- negative examples, где модель ведёт себя как generic assistant или присваивает identity внешнего teacher;
- **EXPERIMENT REQUIRED —** behavior stages сравниваются с BF16 base по coding, tool, governance и identity gates;
- **RISK —** post-training может вызвать catastrophic forgetting pretraining capabilities.

C. What must remain disclosed:
- training-data provenance и licenses;
- external benchmark/teacher usage;
- architectural influences;
- synthetic-data lineage.

Отдельно объясни:
1. Как обучить и заморозить custom 128K tokenizer до pretraining.
2. Как проверить compression/code/multilingual quality и special-token contract.
3. Как проверить, что independent identity реально сформирована.
4. Какие есть риски catastrophic forgetting и потери coding capability.

# LÆTEX ARCHITECTURE

Спроектируй пять planes:

1. FOUNDATION PLANE
- **VERIFIED FACT —** Independent random initialization, custom tokenizer и scratch pretraining.
- **ENGINEERING HYPOTHESIS —** Target internal MoE: 144 routed experts + 1 shared expert, Top-6.
- Как валидировать architecture на proxy перед scale-up.
- **EXPERIMENT REQUIRED —** Parameter count, routing и scale transfer должны пройти frozen gates.
- Как сохранить качество coding после enterprise post-training.

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
- pretraining token volume;
- SFT verified examples;
- executable sandbox trajectories;
- failure/recovery trajectories;
- held-out private evaluation tasks.

# TRAINING PROGRAM

Нужен конкретный порядок:

Phase 0 — evaluation/data/license freeze
Phase 1 — custom tokenizer and architecture proxies
Phase 2 — H200 systems/scale-transfer gate
Phase 3 — full scratch pretraining → BF16 base
Phase 4 — enterprise Action SFT and preference optimization
Phase 5 — executable RL → BF16 master; serving derivative parity separately
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
- full scratch pretraining;
- LoRA / QLoRA for post-training ablations;
- full fine-tuning;
- selective MoE tuning;
- adapter merge;
- distillation;
- teacher-student training.

Дай рекомендацию, что делать в independent LÆTEX E-01, а что отложить до post-E-01 research.

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

# INDEPENDENT E-01

**VERIFIED FACT —** Независимая модель является текущим accepted E-01, а не будущим LÆTEX-2.

Стартовая гипотеза:
- 64 blocks
- hidden size 8192
- hybrid attention 7 local + 1 global
- local window 16 384; context target 262 144
- GQA 64Q / 8KV; head dimension 128
- 144 routed experts + 1 shared expert
- Top-6 routing; expert dff 2048
- vocabulary 128K; BF16 master
- target ~478.9B total / ~34.4B active pending proxy validation

Проверь математически и executable proxy, насколько эта конфигурация реалистична.
Предложи пересмотр только через ADR, если она плохо масштабируется.
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
13. Independent E-01 validation target
14. Top 10 risks with mitigations
15. What not to build yet
16. Exact first seven engineering actions for this week

Последняя строка должна содержать один жёсткий вердикт:
“LÆTEX wins if …”
 # CANONICAL CHECKPOINT SOURCES

Canonical source of truth:
`docs/adr/0007-independent-from-scratch-e01.md`,
`docs/adr/0008-custom-tokenizer.md`,
`docs/adr/0009-qwen-reference-teacher-firewall.md`,
`docs/adr/0010-scratch-pretrain-post-train-lineage.md`.

External benchmark / optional offline teacher reference only:
https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct

Перед teacher/benchmark run проверь актуальную model card, exact revision и license.
Не выдумывай параметры, license, hardware requirements или benchmark claims.
External model card никогда не переопределяет canonical E-01 architecture и не создаёт weight parent.

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
- provider-attested InfiniBand между узлами; наличие fabric не считается фактом до письменной attestation конкретного allocation и NCCL acceptance;
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