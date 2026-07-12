# LÆTEX E-01 — реестр рисков

## 1. Правила управления

- **[VERIFIED FACT]** Реестр содержит десять главных рисков E-01 и пересматривается Release Manager еженедельно.
- **[VERIFIED FACT]** Статусы: `OPEN`, `MITIGATING`, `ACCEPTED`, `BLOCKED`, `CLOSED`.
- **[VERIFIED FACT]** Severity: P0 — безопасность, tenant isolation, необратимый ущерб или юридически недопустимый релиз; P1 — блокировка release gate; P2 — существенная потеря срока/стоимости; P3 — локальный дефект без влияния на hard gates.
- **[VERIFIED FACT]** Только Program Owner может принять residual P1; residual P0 не принимается.
- **[RISK]** Отсутствие измеримого leading indicator означает, что риск контролируется декларативно, а не инженерно.
- **[EXPERIMENT REQUIRED]** Ни один риск ниже не считается закрытым до получения указанного evidence.

## R-01 — деградация coding capability

- **[RISK]** Последовательные `A1` identity/tool, `A2` Enterprise Action SFT, `A3` preference и `A4` executable GRPO могут накопить catastrophic forgetting, identity drift, router degradation или over-specialization.
- **[VERIFIED FACT]** Триггер: нижняя граница 95% CI по любой pre-registered coding-retention метрике ниже immutable baseline gate.
- **[VERIFIED FACT]** Leading indicator: рост loss на held-out code slices, падение compile/test pass rate, увеличение edit churn или regression density.
- **[ENGINEERING HYPOTHESIS]** Короткие adapter stages, frozen S0 comparison, replay исходных code distributions и отдельный gate перед каждым merge ограничат деградацию лучше одного сквозного run.
- **[VERIFIED FACT]** Mitigation: immutable `S0/A1/M1/A2/M2/A3/M3/A4/M4`; retention eval до и после каждого merge; data rebalancing; rollback к последнему прошедшему master; запрет release при gate breach.
- **[VERIFIED FACT]** Владелец: Research Lead.
- **[VERIFIED FACT]** Acceptance: только residual P2 при отсутствии статистически подтверждённой регрессии и при прохождении двух clean runs.
- **[EXPERIMENT REQUIRED]** Stage-wise ablation `A1`, `A2`, `A3`, `A4` и comparison каждого `M1..M4` с immutable `S0` и непосредственным parent.

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

## R-06 — merge corruption, невоспроизводимость или ложная FP8 parity

- **[RISK]** Ошибочный BF16 merge, потерянный adapter, перенос optimizer state через boundary, нефиксированный runtime или promotion FP8 без parity может незаметно испортить release lineage.
- **[VERIFIED FACT]** Триггер: отсутствует hash parent/adapter/merge output, adapter не сохранён, optimizer не reset, post-merge gate расходится с pre-merge tolerance, FP8 нарушает frozen BF16 parity либо run нельзя восстановить из registry.
- **[VERIFIED FACT]** Leading indicator: manual config edits, mutable tags, weight delta вне ожидаемого range, load failures, checkpoint gaps, numerical drift, расхождение BF16/FP8 logits или task verdicts.
- **[VERIFIED FACT]** Mitigation: immutable OCI digests; signed manifests `S0/A1/M1/A2/M2/A3/M3/A4/M4`; retained adapters; fresh optimizer на каждой стадии; deterministic BF16 merge; pre/post-merge regression; отдельный FP8 export и parity suite.
- **[VERIFIED FACT]** Владелец: Platform Lead.
- **[VERIFIED FACT]** Acceptance: residual P1 не принимается; release parent остаётся BF16 `M4`, пока FP8 не прошёл numerical, load, latency и full LÆTEX-Bench parity.
- **[EXPERIMENT REQUIRED]** Restore-and-replay каждого merge и независимый BF16-versus-FP8 parity run в отдельном RunPod H200 allocation.

## R-07 — недоступность RunPod capacity свыше 64 H200

- **[RISK]** Preference/GRPO или rollout topology может потребовать более 64 H200, тогда как публично документированный RunPod Instant Cluster envelope заканчивается на 64 GPU; capacity, InfiniBand и единый failure domain сверх этого размера не доказаны.
- **[VERIFIED FACT]** Триггер: RunPod не подтверждает reserved allocation свыше 64 H200, topology не соответствует manifest, throughput ниже budget floor, возникают repeated NCCL faults или checkpoint SLA не выдержан.
- **[VERIFIED FACT]** Leading indicator: отсутствие письменного capacity commitment, queue delay, cross-cluster topology ambiguity, GPU utilization variance, network retries, storage stalls и растущее время checkpoint.
- **[VERIFIED FACT]** Mitigation: не запускать >64-H200 stage без provider attestation и reservation; topology/NCCL/storage preflight; frequent resumable checkpoints; isolated object storage; budget kill conditions; rollout и update pools разделять только по валидированному design.
- **[VERIFIED FACT]** Владелец: Platform Lead.
- **[VERIFIED FACT]** Acceptance: residual P2 принимается Program Owner только при подписанном capacity plan; mixed/non-H200 cluster и неподтверждённая агрегация нескольких allocations запрещены.
- **[EXPERIMENT REQUIRED]** Throughput, cross-node collective и node-failure recovery benchmark на точной production topology до >64-H200 run.

## R-08 — неработающая экономика 480B/35B

- **[RISK]** Прямой 480B/35B foundation может пройти quality gates, но проиграть baseline по cost per verified task из-за BF16/FP8 serving footprint, rollout generation, retries, verification и operator labor.
- **[VERIFIED FACT]** Триггер: верхняя граница 95% CI стоимости verified task выше pre-registered ceiling, H200-hours на resolved task превышают budget либо VETCR uplift против baseline не доказан.
- **[VERIFIED FACT]** Leading indicator: низкая batch occupancy, рост tokens/task, tool retries, rollout discard rate, sandbox minutes, verifier fan-out, GPU idle time и human intervention.
- **[ENGINEERING HYPOTHESIS]** FP8 после parity, prefix/state caching, retrieval minimization, continuous batching и параллельная verification могут снизить стоимость без потери VETCR.
- **[VERIFIED FACT]** Mitigation: end-to-end H200 metering, cost attribution по task ID и stage, caps, caching, retry/rollout budget, stop-loss до reservation и запрет production GO без clean economic runs.
- **[VERIFIED FACT]** Владелец: Program Owner; технический со-владелец: Platform Lead.
- **[VERIFIED FACT]** Acceptance: residual P1 допустим только для R&D continuation, но не для production GO.
- **[EXPERIMENT REQUIRED]** Два clean BF16/FP8 cost runs на неизменном workload mix с полной стоимостью training amortization, inference, verification и human review.

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
