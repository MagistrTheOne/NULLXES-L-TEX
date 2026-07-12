# LÆTEX E-01 — 90-дневная дорожная карта

## 1. Контракт программы

- **[VERIFIED FACT]** Горизонт программы — 13 недель (90 календарных дней).
- **[VERIFIED FACT]** Обучение, fine-tuning, генерация teacher trajectories и model inference выполняются только в RunPod на выделенных NVIDIA H200.
- **[VERIFIED FACT]** Допустимая вычислительная топология использует H200 HGX с NVLink/NVSwitch внутри узла.
- **[EXPERIMENT REQUIRED]** Перед multi-node run конкретный RunPod allocation обязан предоставить attestation InfiniBand/high-bandwidth fabric и пройти NCCL acceptance.
- **[RISK]** Внешняя документация не подтверждает fabric конкретного allocation; отсутствие attestation означает NO-GO.
- **[VERIFIED FACT]** Локальный control plane используется только для кода, конфигураций, оркестрации, просмотра метрик и unit-тестов без весов модели.
- **[RISK]** Любой локальный запуск модели, локальное обучение или перенос весов на рабочую станцию нарушает compute boundary и блокирует релиз.
- **[ENGINEERING HYPOTHESIS]** E-01 должен доказать превосходство в ограниченном наборе enterprise coding scenarios по verified task completion, стоимости, задержке, приватности и аудируемости; универсальное превосходство над frontier-моделями не является целью.
- **[EXPERIMENT REQUIRED]** Значения производительности и качества считаются неизвестными до двух чистых воспроизводимых прогонов LÆTEX-Bench.

## 2. Роли владельцев

- **[VERIFIED FACT]** Program Owner отвечает за бюджет, scope и финальные GO/NO-GO.
- **[VERIFIED FACT]** Research Lead отвечает за модель, training design и экспериментальную честность.
- **[VERIFIED FACT]** Data Lead отвечает за lineage, лицензии, PII-контроль, дедупликацию и contamination control.
- **[VERIFIED FACT]** Platform Lead отвечает за RunPod H200, storage, registry, observability и воспроизводимость.
- **[VERIFIED FACT]** Evaluation Lead отвечает за immutable baseline, LÆTEX-Bench, статистику и clean-run protocol.
- **[VERIFIED FACT]** Safety & Governance Lead отвечает за policy engine, identity tests, red team и release evidence.
- **[VERIFIED FACT]** Product/Workflow Lead отвечает за CodeWorld workflows, tool contracts и enterprise acceptance.
- **[VERIFIED FACT]** Security Lead отвечает за tenant isolation, credentials, secrets boundaries и incident response.
- **[VERIFIED FACT]** Release Manager собирает подписанный evidence bundle и исполняет release gates.

## 3. Недельный план

### Неделя 1 — зафиксировать контракт доказательства

- **[VERIFIED FACT]** Артефакты: [`eval/laetex-bench/baseline-manifest.yaml`](../eval/laetex-bench/baseline-manifest.yaml), metric definitions, clean-run protocol, owners/RACI, RunPod H200 boundary policy.
- **[VERIFIED FACT]** Владелец: Evaluation Lead; со-владельцы: Platform Lead, Safety & Governance Lead.
- **[VERIFIED FACT]** Зависимости: утверждённый scope E-01, доступ к RunPod, checkpoint registry и isolated object storage.
- **[ENGINEERING HYPOTHESIS]** Immutable baseline должен включать хэши checkpoint, tokenizer, dataset snapshots, task manifests, graders, tool schemas, runtime image и inference config.
- **[EXPERIMENT REQUIRED]** Dry-run доказательственного конвейера без model training.
- **[RISK]** Изменяемая baseline-конфигурация делает результаты несопоставимыми.
- **[VERIFIED FACT]** GO: manifest подписан владельцами, dry-run формирует полный bundle. NO-GO: отсутствует хотя бы один хэш, owner или источник lineage.

### Неделя 2 — собрать evaluation-first baseline

- **[VERIFIED FACT]** Артефакты: held-out task registry, contamination rules, baseline runner, grader contracts, severity taxonomy P0–P3.
- **[VERIFIED FACT]** Владелец: Evaluation Lead; зависимости: неделя 1, доступ к исходному base checkpoint только в H200-контуре.
- **[EXPERIMENT REQUIRED]** Первый диагностический baseline run нужен только для выявления дефектов benchmark harness и не считается release evidence.
- **[RISK]** Model-based grader без автоматических проверок может завысить completion rate.
- **[VERIFIED FACT]** GO: все задачи replayable, автоматические graders детерминированы либо имеют зафиксированный tolerance. NO-GO: task leakage, неразрешённая лицензия или нереплеябельные задачи.

### Неделя 3 — запустить data governance и corpus intake

- **[VERIFIED FACT]** Артефакты: dataset cards, source allowlist/denylist, PII pipeline, license policy, deduplication report format, tenant opt-in contract.
- **[VERIFIED FACT]** Владелец: Data Lead; зависимости: baseline contamination rules.
- **[VERIFIED FACT]** Сырые данные enterprise-клиента запрещено включать в общий LÆTEX Corpus без явного opt-in и отдельного legal/data approval.
- **[EXPERIMENT REQUIRED]** Проверить PII/secrets detectors на размеченной контрольной выборке.
- **[RISK]** Неотслеживаемая синтетика может воспроизвести лицензируемые или приватные данные teacher.
- **[VERIFIED FACT]** GO: каждый sample имеет source, license, transformation, consent, tenant scope и lineage ID. NO-GO: orphan samples или неустранённые PII/secrets.

### Неделя 4 — зафиксировать CodeWorld и tool contracts

- **[VERIFIED FACT]** Артефакты: CodeWorld state schema, event ledger schema, read/write tool schemas, approval levels, evidence contract.
- **[VERIFIED FACT]** Владелец: Product/Workflow Lead; зависимости: security boundary и benchmark task types.
- **[ENGINEERING HYPOTHESIS]** Структурированное состояние уменьшит prompt stuffing и повысит воспроизводимость действий.
- **[EXPERIMENT REQUIRED]** Replay issue → patch → test → CI outcome с обновлением state после каждого действия.
- **[RISK]** Несвежий state создаёт правдоподобные, но неверные действия.
- **[VERIFIED FACT]** GO: state refresh и audit entry обязательны после каждого write action. NO-GO: write tool может обойти policy pre-check или ledger.

### Неделя 5 — подготовить CPT/SFT production pipeline

- **[VERIFIED FACT]** Артефакты: Megatron-LM/DeepSpeed job specs, data mixer, checkpoint strategy, recovery drill, run-cost estimator.
- **[VERIFIED FACT]** Владелец: Research Lead; со-владелец: Platform Lead; зависимости: corpus intake и RunPod H200 quota.
- **[VERIFIED FACT]** Минимальная и рекомендуемая H200-конфигурации фиксируются в run manifest до выделения бюджета; DP/TP/PP/EP фиксируются для каждого run.
- **[EXPERIMENT REQUIRED]** Короткий pipeline validation run на H200 с синтетическим обезличенным shard; это не quality experiment.
- **[RISK]** Непроверенный resume может потерять дорогой training run.
- **[VERIFIED FACT]** GO: checkpoint restore, metric continuity и artifact upload подтверждены. NO-GO: локальный fallback, untracked image или неполный checkpoint.

### Неделя 6 — выполнить ограниченный CPT run

- **[VERIFIED FACT]** Артефакты: CPT checkpoint candidate, run manifest, data lineage snapshot, loss/throughput telemetry, cost ledger.
- **[VERIFIED FACT]** Владелец: Research Lead; зависимости: недели 3 и 5.
- **[ENGINEERING HYPOTHESIS]** Ограниченный enterprise/code CPT улучшит domain fit без заметной потери coding capability.
- **[EXPERIMENT REQUIRED]** Сравнить candidate с immutable base baseline на coding retention, perplexity slices и identity probes.
- **[RISK]** Catastrophic forgetting или router degradation может уничтожить преимущество foundation checkpoint.
- **[VERIFIED FACT]** GO: нет статистически подтверждённой регрессии на predeclared retention gates. NO-GO: gate breach; checkpoint изолируется и не продвигается.

### Неделя 7 — выполнить verified SFT

- **[VERIFIED FACT]** Артефакты: SFT checkpoint candidate, verified-example manifest, failure taxonomy, tool-call conformance report.
- **[VERIFIED FACT]** Владелец: Research Lead; зависимости: CPT candidate и verified SFT set.
- **[ENGINEERING HYPOTHESIS]** Full SFT с собственным response/tool contract должен изменить поведение без смены tokenizer.
- **[EXPERIMENT REQUIRED]** Проверить tool validity, identity overwrite и coding retention на held-out наборах.
- **[RISK]** Синтетические ответы teacher могут закрепить формат без реальной task completion.
- **[VERIFIED FACT]** GO: candidate проходит промежуточные gates и улучшает verified outcomes. NO-GO: улучшение только style/model-grader score без executable evidence.

### Неделя 8 — preference optimization и failure recovery

- **[VERIFIED FACT]** Артефакты: preference dataset, recovery trajectories, candidate checkpoint, reward audit.
- **[VERIFIED FACT]** Владелец: Research Lead; со-владелец: Safety & Governance Lead; зависимости: SFT candidate.
- **[ENGINEERING HYPOTHESIS]** Preferences по evidence quality, reversibility и escalation улучшат безопасное выполнение.
- **[EXPERIMENT REQUIRED]** Проверить reward hacking, over-refusal, under-escalation и recovery after tool failure.
- **[RISK]** Оптимизация proxy reward может снизить реальный VETCR.
- **[VERIFIED FACT]** GO: VETCR не падает, policy behavior улучшается на held-out cases. NO-GO: reward растёт при ухудшении executable metrics.

### Неделя 9 — executable RL / GRPO в sandbox

- **[VERIFIED FACT]** Артефакты: sandbox image registry, GRPO run manifest, trajectory ledger, verifier report, candidate checkpoint.
- **[VERIFIED FACT]** Владелец: Research Lead; зависимости: sandbox isolation, deterministic graders, policy pre-check.
- **[ENGINEERING HYPOTHESIS]** Executable reward улучшит завершение задач и устойчивость после tool failures.
- **[EXPERIMENT REQUIRED]** Оценить gain на unseen tasks, rollback correctness и policy escape rate.
- **[RISK]** Sandbox exploit или grader gaming создаёт ложное качество.
- **[VERIFIED FACT]** GO: reward подтверждается независимыми graders и replay. NO-GO: escape, non-replayable gain или contamination.

### Неделя 10 — router и Organizational World Model V0

- **[VERIFIED FACT]** Артефакты: adapter routing policy, route audit fields, graph/event-ledger/policy-engine V0, stale-state detector.
- **[VERIFIED FACT]** Владелец: Product/Workflow Lead; со-владельцы: Research Lead, Safety & Governance Lead.
- **[ENGINEERING HYPOTHESIS]** Top-2 domain adapters плюс shared Evidence/Policy adapter полезны только при измеримом выигрыше над single-adapter control.
- **[EXPERIMENT REQUIRED]** Проверить router collapse, route stability, explainability и ablation against no-router control.
- **[RISK]** Learned router может маршрутизировать по поверхностным метаданным и скрыть причину ошибки.
- **[VERIFIED FACT]** GO: routing даёт воспроизводимый gain и полный audit trail. NO-GO: отсутствие gain; E-01 остаётся на статической routing policy.

### Неделя 11 — интеграционный hardening

- **[VERIFIED FACT]** Артефакты: tenant-isolation test report, short-lived credential flow, rollback playbook, evidence signer, cost-per-task instrumentation.
- **[VERIFIED FACT]** Владелец: Platform Lead; со-владельцы: Security Lead, Release Manager.
- **[EXPERIMENT REQUIRED]** Выполнить rollback drill, credential expiry tests, cross-tenant negative tests и fault injection.
- **[RISK]** Корректная модель не компенсирует небезопасный execution plane.
- **[VERIFIED FACT]** GO: rollback drill успешен, zero cross-tenant reads/writes, evidence bundle подписывается. NO-GO: любой P0 escape или невозможность восстановления.

### Неделя 12 — clean run №1 и red team

- **[VERIFIED FACT]** Артефакты: clean-run evidence bundle №1, identity 10k report, policy red-team report, VETCR с 95% CI, tool-validity report, cost report.
- **[VERIFIED FACT]** Владелец: Evaluation Lead; со-владелец: Safety & Governance Lead.
- **[EXPERIMENT REQUIRED]** Это первый допустимый release-evidence run на неизменной baseline.
- **[RISK]** Любое изменение checkpoint, data, task, grader, runtime или threshold после старта аннулирует clean run.
- **[VERIFIED FACT]** GO: все release gates пройдены. NO-GO: исправить причину, выпустить новый versioned candidate и начать два clean runs заново.

### Неделя 13 — clean run №2 и решение E-01

- **[VERIFIED FACT]** Артефакты: clean-run evidence bundle №2, variance analysis, signed release dossier, GO/NO-GO протокол.
- **[VERIFIED FACT]** Владелец: Release Manager; финальный approver: Program Owner.
- **[EXPERIMENT REQUIRED]** Второй независимый clean run обязан воспроизвести все hard gates без изменения baseline.
- **[RISK]** Один успешный run недостаточен для релиза.
- **[VERIFIED FACT]** GO: два последовательных clean runs прошли все gates, bundles подписаны, rollback и deployment approvals действительны. NO-GO: любой hard gate не пройден; E-01 не получает release status.

## 4. Сквозные зависимости и бюджетные остановки

- **[VERIFIED FACT]** Порядок критического пути: immutable baseline → governed corpus → reproducible H200 pipeline → CPT/SFT/RL candidates → integration hardening → два clean runs.
- **[RISK]** Запуск дорогого H200 training до готовности evaluation и lineage создаёт checkpoint без доказательной ценности.
- **[VERIFIED FACT]** H200 run экономически разрешён только при наличии pre-registered objective, stop condition, budget cap, artifact destination и rollback/resume plan.
- **[ENGINEERING HYPOTHESIS]** Недельные gates снижают sunk-cost risk лучше, чем один финальный benchmark.
- **[EXPERIMENT REQUIRED]** Фактические wall-clock, throughput и cost curves должны быть измерены на выбранной RunPod H200 topology; оценки не выдаются за результаты.

## 5. 90-дневный terminal gate

- **[VERIFIED FACT]** Решение GO требует выполнения всех критериев `RELEASE-GATES.md`.
- **[VERIFIED FACT]** Решение CONDITIONAL GO допускается только для продолжения R&D и не разрешает production release.
- **[VERIFIED FACT]** Решение NO-GO обязательно при policy P0, identity failure, отсутствии двух clean runs, неподписанном evidence bundle или нарушении H200-only boundary.
- **[RISK]** Срок 90 дней не имеет приоритета над release gates.
