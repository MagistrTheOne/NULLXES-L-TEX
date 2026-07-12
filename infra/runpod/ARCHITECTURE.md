# RunPod-only compute architecture для LÆTEX E-01

## 1. Область решения

- **[VERIFIED FACT]** Единственный accelerator для E-01 — NVIDIA H200 SXM с 141 GB HBM на GPU. Другие GPU, смешанные кластеры и локальные model workloads запрещены.
- **[VERIFIED FACT]** Multi-node workloads выполняются только в RunPod H200 Instant Clusters: 2–8 узлов по 8 GPU, то есть 16–64 H200; для большего масштаба требуется отдельное согласование с RunPod.
- **[VERIFIED FACT]** RunPod документирует для H200 Instant Clusters inter-node fabric до 3200 Gbps и выделяет интерфейсы `ens1`–`ens8` для cluster traffic.
- **[VERIFIED FACT]** Network Volume доступен для Pods только в Secure Cloud, подключается к Instant Cluster при создании и монтируется на каждом узле как `/workspace`.
- **[RISK]** «До 3200 Gbps» — характеристика сервиса, а не гарантия NCCL throughput конкретного allocation. Перед дорогим run обязателен NCCL acceptance test.
- **[VERIFIED FACT]** Локальная машина — только control plane: Git, declarative profiles, submission, просмотр обезличенных метрик и лёгкие unit tests. На ней не хранятся веса, optimizer states, training shards и inference cache; не выполняются inference, training, CPT, SFT, RL или teacher generation.

## 2. Три изолированных контура

### 2.1 H200 training cluster

- **[ENGINEERING HYPOTHESIS]** Production multi-node default — H200 Instant Cluster с homogeneous 8-GPU nodes, NVLink/NVSwitch внутри узла и RunPod high-speed fabric между узлами.
- **[ENGINEERING HYPOTHESIS]** Один 8×H200 Secure Cloud Pod допустим только для ограниченных adapter/preference/router jobs и release smoke, если allocation подтверждает HGX/NVSwitch topology; Phase 0 baseline использует minimum 16 H200, а CPT/GRPO scale остаётся multi-node Instant Cluster.
- **[VERIFIED FACT]** Оркестратор получает `NODE_RANK`, `WORLD_SIZE`, `MASTER_ADDR`/`PRIMARY_ADDR` и другие distributed environment variables от Instant Cluster.
- **[ENGINEERING HYPOTHESIS]** Training stack — pinned OCI image, Megatron-Core/Megatron-LM + Transformer Engine; DeepSpeed допустим только после phase-specific parity test.
- **[RISK]** Нельзя считать Ethernet-интерфейс `eth0` training fabric. NCCL должен быть привязан к подтверждённым `ens*` интерфейсам.
- **[RISK]** Публичная документация RunPod подтверждает high-speed `ens*` fabric и aggregate figure до 3200 Gbps, но не доказывает InfiniBand protocol/topology конкретного allocation.
- **[VERIFIED FACT]** E-01 требует InfiniBand между узлами; allocation без письменной attestation InfiniBand и успешного NCCL/IB acceptance test является NO-GO.

### 2.2 H200 inference/evaluation cluster

- **[ENGINEERING HYPOTHESIS]** Baseline, rollout workers, release evaluation и offline teacher inference используют отдельные H200 allocations; training и serving не делят GPU.
- **[VERIFIED FACT]** Teacher Qwen3-Coder-480B-A35B-Instruct имеет 480B total / 35B activated parameters и применяется только offline для generation, critique, distillation labels и hard-case evaluation.
- **[RISK]** Teacher запрещён как live runtime и не включается в пользовательский request path.

### 2.3 Local control plane

- **[VERIFIED FACT]** Control plane хранит только конфигурации, run IDs, checksums, агрегированные метрики и ссылки на registry objects.
- **[RISK]** API keys, cloud credentials и registry credentials не записываются в Git/YAML; они инжектируются через RunPod secrets или внешний secrets manager.

## 3. Storage topology

| Уровень | Назначение | Политика |
|---|---|---|
| RunPod Network Volume `/workspace` | staging datasets, tokenizer/cache, active checkpoints, dataloader working set, temporary rollout artifacts | **[VERIFIED FACT]** Persistent independently of compute; используется как рабочий набор, но не как единственная копия. |
| Local NVMe/container scratch | per-rank cache, temporary compilation artifacts, transient activation spill только если phase profile разрешает | **[RISK]** Ephemeral; никогда не является registry. |
| External encrypted object store | immutable datasets, manifests, source checkpoints, promoted checkpoints, eval bundles, audit logs | **[ENGINEERING HYPOTHESIS]** Durable source of truth с versioning, object lock, server-side encryption и separate service identity per environment. |

- **[VERIFIED FACT]** Network Volume не заменяет durable registry; RunPod предупреждает, что volume может быть утрачен при неоплате хранения.
- **[ENGINEERING HYPOTHESIS]** Каждый run сначала materializes immutable manifest из object store в `/workspace/runs/<run-id>/inputs`, проверяет SHA-256/BLAKE3, а после checkpoint/eval атомарно публикует manifest и объекты обратно.
- **[RISK]** Concurrent writers к одному volume могут повредить данные. Один run получает один write namespace; promotion выполняет единственный registry writer.
- **[EXPERIMENT REQUIRED]** Измерить sustained read throughput Network Volume на packed-shard workload; если dataloader starvation >2% step time, добавить node-local read-through cache, не меняя durable topology.

## 4. Security и tenancy

- **[VERIFIED FACT]** Используется только RunPod Secure Cloud; Community Cloud запрещён.
- **[ENGINEERING HYPOTHESIS]** Отдельные RunPod projects/accounts, Network Volumes, object-store prefixes, KMS keys и service identities для `dev`, `eval`, `train`, `release`.
- **[RISK]** Secure Cloud и container isolation не дают автоматической tenant-level data governance. Клиентские данные не поступают в общий corpus без explicit opt-in и отдельного lineage record.
- **[ENGINEERING HYPOTHESIS]** Egress deny-by-default после materialization; allowlist только registry, telemetry sink и approved package mirror.
- **[ENGINEERING HYPOTHESIS]** Short-lived credentials, no SSH by default, no public notebook, immutable image digest, SBOM, signature verification и audit event на submit/start/checkpoint/promote/terminate.
- **[EXPERIMENT REQUIRED]** До Phase 1 провести threat model и доказать, что logs, crash dumps и telemetry не содержат prompts, source code, tokens или secrets.

## 5. Declarative profile contract

Файлы `infra/runpod/profiles/*.yaml` являются документационными профилями, а не provisioning manifests.

- **[VERIFIED FACT]** Они не вызывают RunPod API и не содержат secrets.
- **[ENGINEERING HYPOTHESIS]** Общая schema version — `laetex.runpod.profile/v1`; обязательные поля: `name`, `phase`, `classification`, `platform`, `compute`, `parallelism`, `network`, `storage`, `checkpoint`, `wall_clock`, `metrics`, `stop_conditions`, `economic_gate`, `artifacts`, `validation`.
- **[VERIFIED FACT]** `wall_clock` содержит собственный `tag: ENGINEERING_HYPOTHESIS`; оценка не является измеренным runtime.
- **[VERIFIED FACT]** Верхнеуровневый `classification` является epistemic tag для всех не переопределённых полей профиля; элементы `assumptions` обязаны иметь собственный `tag`.
- **[RISK]** Числа GPU и parallelism — budget envelope, а не доказанная работоспособность. Run-specific config создаётся только после dry validation и smoke run на H200.

### Validation notes

Перед submission CI должен отклонять профиль, если:

1. **[VERIFIED FACT]** `gpu.model != NVIDIA H200 SXM` или `gpu.hbm_gb != 141`.
2. **[VERIFIED FACT]** указан Community Cloud, локальный inference/training или иной accelerator.
3. **[ENGINEERING HYPOTHESIS]** `recommended_gpus > 8` без `deployment.recommended: instant-cluster`; single-node minimum требует `deployment.minimum: secure-cloud-pod`.
4. **[ENGINEERING HYPOTHESIS]** `recommended_gpus` не кратно восьми либо Instant Cluster выходит за документированный диапазон 16–64 GPU.
5. **[VERIFIED FACT]** отсутствуют Network Volume working set и external encrypted object-store registry.
6. **[VERIFIED FACT]** присутствует literal credential, token, private endpoint с embedded auth или secret value.
7. **[ENGINEERING HYPOTHESIS]** `TP × PP × CP × DP != world_size`; `EP` дополнительно проверяется на совместимость с Megatron expert/data parallel groups.
8. **[ENGINEERING HYPOTHESIS]** нет exact metric, stop condition, checkpoint cadence, artifact manifest или economic gate.
9. **[VERIFIED FACT]** teacher указан в online/live serving path.

## 6. Cluster acceptance gate

- **[EXPERIMENT REQUIRED]** На каждом новом allocation выполнить topology discovery, InfiniBand device/link attestation, GPU/HBM check, image digest check, NCCL all-reduce/all-to-all, Network Volume read/write test и object-store round-trip checksum.
- **[ENGINEERING HYPOTHESIS]** Acceptance: 0 GPU/XID/ECC errors; все ranks видимы; 141 GB HBM reported; NCCL без fallback на `eth0`; collective bandwidth не ниже 80% от согласованного внутреннего baseline; checksum mismatch = 0.
- **[RISK]** Не запускать платную training phase, если acceptance gate не пройден или RunPod capacity не зарезервирована на ожидаемый wall-clock + checkpoint buffer.

## 7. Checkpoint lifecycle

1. **[ENGINEERING HYPOTHESIS]** Distributed checkpoint пишется в run-scoped staging на `/workspace`.
2. **[VERIFIED FACT]** Checkpoint считается валидным только после успешного load/resume test.
3. **[ENGINEERING HYPOTHESIS]** Registry writer загружает shards, optimizer/RNG/data-cursor state и manifest в encrypted object store.
4. **[ENGINEERING HYPOTHESIS]** Promotion pointer обновляется только после checksum и eval gate; partial checkpoints имеют TTL.
5. **[RISK]** Adapter, base checkpoint, tokenizer, chat template и tool schema версионируются как единый release bundle; несовместимое смешивание запрещено.

## 8. Source-of-truth snapshot

- **[VERIFIED FACT]** Qwen3-Coder-Next-Base model card: Apache-2.0, pretraining-only, 80B total / 3B activated, 48 layers, 512 routed experts, 10 activated + 1 shared, native 262,144 context.
- **[VERIFIED FACT]** Qwen3-Coder-480B-A35B-Instruct model card: 480B total / 35B activated, 62 layers, 160 experts, 8 activated, native 262,144 context.
- **[RISK]** Model cards и RunPod service limits меняются. Перед каждым release зафиксировать URL, retrieval date, content hash и расхождения с этой документацией.

