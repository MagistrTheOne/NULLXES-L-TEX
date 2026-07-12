# LÆTEX E-01 — реестр рисков

## 1. Правила управления

- **[VERIFIED FACT]** Реестр содержит десять главных рисков E-01 и пересматривается Release Manager еженедельно.
- **[VERIFIED FACT]** Статусы: `OPEN`, `MITIGATING`, `ACCEPTED`, `BLOCKED`, `CLOSED`.
- **[VERIFIED FACT]** Severity: P0 — безопасность, tenant isolation, необратимый ущерб или юридически недопустимый релиз; P1 — блокировка release gate; P2 — существенная потеря срока/стоимости; P3 — локальный дефект без влияния на hard gates.
- **[VERIFIED FACT]** Только Program Owner может принять residual P1; residual P0 не принимается.
- **[RISK]** Отсутствие измеримого leading indicator означает, что риск контролируется декларативно, а не инженерно.
- **[EXPERIMENT REQUIRED]** Ни один риск ниже не считается закрытым до получения указанного evidence.

## R-01 — деградация coding capability

- **[RISK]** CPT/SFT/preference/RL может вызвать catastrophic forgetting, router degradation или over-specialization.
- **[VERIFIED FACT]** Триггер: нижняя граница 95% CI по любой pre-registered coding-retention метрике ниже immutable baseline gate.
- **[VERIFIED FACT]** Leading indicator: рост loss на held-out code slices, падение compile/test pass rate, увеличение edit churn или regression density.
- **[ENGINEERING HYPOTHESIS]** Selective tuning, replay исходных code distributions и короткие staged runs ограничат деградацию лучше одного большого run.
- **[VERIFIED FACT]** Mitigation: checkpoint cadence; retention eval на каждом promotion; data rebalancing; rollback к последнему прошедшему candidate; запрет release при gate breach.
- **[VERIFIED FACT]** Владелец: Research Lead.
- **[VERIFIED FACT]** Acceptance: только residual P2 при отсутствии статистически подтверждённой регрессии и при прохождении двух clean runs.
- **[EXPERIMENT REQUIRED]** Ablation CPT-only/SFT-only/combined и comparison с immutable base.

## R-02 — ложный VETCR и contamination

- **[RISK]** Утечка задач, нестабильные graders или model-grader bias могут создать ложное преимущество.
- **[VERIFIED FACT]** Триггер: обнаружен overlap с training data, изменился task hash, replay расходится с исходным verdict или grader disagreement превышает pre-registered tolerance.
- **[VERIFIED FACT]** Leading indicator: аномально резкий gain на узком slice, near-duplicate matches, высокая доля решений с memorized strings, расхождение automatic и human review.
- **[VERIFIED FACT]** Mitigation: immutable held-out registry, dedup fingerprints, canary tasks, deterministic executable graders, blinded human audit, versioned benchmark.
- **[VERIFIED FACT]** Владелец: Evaluation Lead.
- **[VERIFIED FACT]** Acceptance: P0 не принимается; contaminated run аннулируется полностью.
- **[EXPERIMENT REQUIRED]** Независимый contamination scan до каждого clean run и после freeze training corpus.

## R-03 — policy escape или разрушительное действие

- **[RISK]** Модель или tool runtime может выполнить действие без разрешения, выйти за scope или обойти approval.
- **[VERIFIED FACT]** Триггер: любой P0 policy escape, unauthorized write, destructive action без approval либо использование credentials вне scope/TTL.
- **[VERIFIED FACT]** Leading indicator: рост denied calls, malformed approval claims, попытки вызвать write tool из read-only state, несоответствие expected_delta фактическому delta.
- **[ENGINEERING HYPOTHESIS]** Внешний policy enforcement эффективнее обучения модели как единственной линии защиты.
- **[VERIFIED FACT]** Mitigation: deny-by-default policy engine, typed tools, short-lived credentials, sandbox, approval tokens, pre-action simulation, post-action reconciliation, kill switch.
- **[VERIFIED FACT]** Владелец: Safety & Governance Lead; технический со-владелец: Security Lead.
- **[VERIFIED FACT]** Acceptance: residual P0 запрещён; release требует zero P0 policy escapes.
- **[EXPERIMENT REQUIRED]** Adversarial tool-use suite, privilege-escalation tests и fault injection.

## R-04 — нарушение tenant isolation и утечка данных

- **[RISK]** Данные, embeddings, cache, logs, credentials или artifacts одного tenant могут попасть другому tenant или в общий corpus.
- **[VERIFIED FACT]** Триггер: любой cross-tenant read/write, cache collision, lineage без tenant scope или обучение на client data без explicit opt-in.
- **[VERIFIED FACT]** Leading indicator: missing tenant IDs, shared unpartitioned cache keys, orphan objects, denied IAM events, несогласованность retention policy.
- **[VERIFIED FACT]** Mitigation: tenant-scoped storage, encryption keys, namespaces, cache partitioning, egress controls, explicit opt-in ledger, deletion workflow и negative tests.
- **[VERIFIED FACT]** Владелец: Security Lead.
- **[VERIFIED FACT]** Acceptance: residual P0 запрещён; любой подтверждённый cross-tenant event блокирует релиз и активирует incident response.
- **[EXPERIMENT REQUIRED]** Cross-tenant penetration tests и проверка deletion propagation.

## R-05 — недействительные tool calls и stale state

- **[RISK]** Невалидные параметры, устаревший CodeWorld state или неверное expected_delta ведут к ошибочным действиям.
- **[VERIFIED FACT]** Триггер: tool-call validity ниже 99,5%, state-version mismatch не блокируется либо post-action reconciliation отсутствует.
- **[VERIFIED FACT]** Leading indicator: schema rejects, retries, stale reads, tool failures, delta mismatch, рост ручных исправлений.
- **[ENGINEERING HYPOTHESIS]** Versioned state handles и schema-constrained decoding уменьшат этот риск.
- **[VERIFIED FACT]** Mitigation: strict JSON schema, state ETags, optimistic concurrency, idempotency keys, read-before-write, tool simulators, typed error recovery.
- **[VERIFIED FACT]** Владелец: Product/Workflow Lead.
- **[VERIFIED FACT]** Acceptance: residual P1 допускается только ниже 0,5% invalid calls и без P0/P1 side effects.
- **[EXPERIMENT REQUIRED]** Tool fuzzing, stale-state race tests и recovery replay.

## R-06 — невоспроизводимое обучение или inference

- **[RISK]** Нефиксированные images, configs, seeds, data snapshots или runtime параметры делают результат недоказуемым.
- **[VERIFIED FACT]** Триггер: artifact не имеет content hash, run невозможно восстановить из registry либо два clean runs расходятся за pre-registered tolerance.
- **[VERIFIED FACT]** Leading indicator: manual config edits, mutable tags, missing environment capture, checkpoint/upload gaps, недетерминированный grader.
- **[VERIFIED FACT]** Mitigation: immutable OCI digests, tracked manifests, dataset/checkpoint registry, seed policy, signed provenance, automated environment capture.
- **[VERIFIED FACT]** Владелец: Platform Lead.
- **[VERIFIED FACT]** Acceptance: residual P1 не принимается для release evidence; оба clean runs обязаны быть воспроизводимыми.
- **[EXPERIMENT REQUIRED]** Restore-and-replay drill в отдельном RunPod H200 allocation.

## R-07 — RunPod H200 capacity, network или storage failure

- **[RISK]** Недоступность H200, деградация InfiniBand/NVLink, storage bottleneck или spot interruption может сорвать run и бюджет.
- **[VERIFIED FACT]** Триггер: allocation не соответствует manifest, throughput ниже budget floor, repeated NCCL faults, checkpoint SLA не выдержан.
- **[VERIFIED FACT]** Leading indicator: queue delay, GPU utilization variance, network retries, storage read stalls, растущее время checkpoint.
- **[VERIFIED FACT]** Mitigation: reserved H200 capacity для critical runs, topology validation, health checks, frequent resumable checkpoints, isolated object storage, budget kill conditions.
- **[VERIFIED FACT]** Владелец: Platform Lead.
- **[VERIFIED FACT]** Acceptance: residual P2 принимается Program Owner только при сохранении 90-day critical path; смешанный или не-H200 кластер запрещён.
- **[EXPERIMENT REQUIRED]** Throughput benchmark и node-failure recovery до production training.

## R-08 — перерасход стоимости на verified task

- **[RISK]** Модель может проходить quality gates, но быть экономически хуже baseline из-за inference, retries, verification или operator labor.
- **[VERIFIED FACT]** Триггер: верхняя граница 95% CI стоимости verified task выше pre-registered ceiling либо improvement против baseline не доказан.
- **[VERIFIED FACT]** Leading indicator: рост tokens/task, tool retries, sandbox minutes, verifier fan-out, GPU idle time и human intervention.
- **[ENGINEERING HYPOTHESIS]** Prefix/state caching, retrieval minimization и параллельная verification снизят стоимость без потери VETCR.
- **[VERIFIED FACT]** Mitigation: end-to-end metering, cost attribution по task ID, caps, routing, caching, retry budget, stop-loss на H200 run.
- **[VERIFIED FACT]** Владелец: Program Owner; технический со-владелец: Platform Lead.
- **[VERIFIED FACT]** Acceptance: residual P1 допустим только для R&D continuation, но не для production GO.
- **[EXPERIMENT REQUIRED]** Два clean cost runs на неизменном workload mix.

## R-09 — identity overwrite неполон

- **[RISK]** Модель может называть себя Qwen, раскрывать upstream persona или вести себя как generic assistant.
- **[VERIFIED FACT]** Триггер: хотя бы 1 identity failure на 10 000 pre-registered adversarial prompts.
- **[VERIFIED FACT]** Leading indicator: upstream self-reference, refusal/persona patterns, chat-template leakage, нестабильность имени между языками и tool contexts.
- **[VERIFIED FACT]** Mitigation: собственный chat template и role contract, negative SFT/preference examples, identity suite, runtime output checks без сокрытия internal legal provenance.
- **[VERIFIED FACT]** Владелец: Safety & Governance Lead.
- **[VERIFIED FACT]** Acceptance: нулевая; release threshold — 0/10 000.
- **[EXPERIMENT REQUIRED]** Multilingual, prompt-injection, role-confusion и serialization adversarial suite.

## R-10 — rollback и evidence chain неработоспособны

- **[RISK]** Ошибку нельзя безопасно отменить, а результат нельзя доказать подписанным audit trail.
- **[VERIFIED FACT]** Триггер: rollback drill не восстанавливает state в RTO/RPO, evidence bundle неполон/неподписан или action невозможно связать с approval и observed_delta.
- **[VERIFIED FACT]** Leading indicator: non-idempotent writes, missing before-state, ledger gaps, signature verification errors, orphan approvals.
- **[VERIFIED FACT]** Mitigation: reversible-by-default actions, snapshots, compensating transactions, append-only event ledger, signed bundle manifest, periodic restore drills.
- **[VERIFIED FACT]** Владелец: Release Manager; технические со-владельцы: Platform Lead, Product/Workflow Lead.
- **[VERIFIED FACT]** Acceptance: residual P1 не принимается; rollback drill и signature verification — hard gates.
- **[EXPERIMENT REQUIRED]** Полный drill на репрезентативной PR-level задаче с fault injection.

## 2. Эскалация

- **[VERIFIED FACT]** P0 немедленно останавливает write actions, training promotion и release process.
- **[VERIFIED FACT]** P1 требует mitigation owner, deadline и повторного gate run.
- **[VERIFIED FACT]** P2 может быть принят Program Owner только с зафиксированным budget/schedule impact.
- **[RISK]** Понижение severity без нового evidence запрещено.
- **[VERIFIED FACT]** Закрытие риска требует ссылки на versioned evidence bundle, а не текстового заверения.
