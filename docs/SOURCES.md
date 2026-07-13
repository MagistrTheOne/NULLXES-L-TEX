# Официальные источники и pinning

> Проверено: 2026-07-13  
> Scope: foundation checkpoints, NVIDIA H200, RunPod H200 compute/network/storage  
> Правило: model card и config проверяются вместе; mutable `main` не заменяет закреплённый revision.

## 1. Прямой foundation E-01

### Закреплённый объект

**VERIFIED FACT —** Repo ID: `Qwen/Qwen3-Coder-480B-A35B-Instruct`.

**VERIFIED FACT —** Official Hugging Face API evidence, проверенный 2026-07-13, закрепляет revision `9d90cf8fca1bf7b7acca42d3fc9ae694a2194069` для `Qwen/Qwen3-Coder-480B-A35B-Instruct`.

**RISK —** Этот 40-hex commit SHA является immutable Hugging Face revision identifier, но не SHA-256 hash весов. Mutable `main` запрещён как training input.

**EXPERIMENT REQUIRED —** Training остаётся заблокированным до RunPod source preflight: скачать и проверить все 241 weight shards, записать их SHA-256, захешировать config, tokenizer и chat template, а также архивировать и захешировать license/notices для exact revision.

Официальные URL:

- **VERIFIED FACT —** Model card: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct>
- **VERIFIED FACT —** Raw model card: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/raw/9d90cf8fca1bf7b7acca42d3fc9ae694a2194069/README.md>
- **VERIFIED FACT —** Config: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/blob/9d90cf8fca1bf7b7acca42d3fc9ae694a2194069/config.json>
- **VERIFIED FACT —** Raw config: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/raw/9d90cf8fca1bf7b7acca42d3fc9ae694a2194069/config.json>
- **VERIFIED FACT —** Repository API metadata: <https://huggingface.co/api/models/Qwen/Qwen3-Coder-480B-A35B-Instruct>
- **VERIFIED FACT —** File tree: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/tree/9d90cf8fca1bf7b7acca42d3fc9ae694a2194069>

### Проверенные параметры foundation

**VERIFIED FACT —** Model card определяет checkpoint как causal language model со стадиями `Pretraining & Post-training`, 480B total parameters, 35B activated parameters, 62 layers, GQA 96 Q heads / 8 KV heads и native context 262 144.

**VERIFIED FACT —** Config задаёт `Qwen3MoeForCausalLM`, `model_type=qwen3_moe`, hidden size 6144, head dimension 128, 62 layers, 160 routed experts, Top-8, expert intermediate size 2560, vocabulary size 151 936, maximum positions 262 144 и `torch_dtype=bfloat16`.

**VERIFIED FACT —** Config задаёт `shared_expert_intermediate_size=0`; shared expert в этой архитектуре отсутствует.

**VERIFIED FACT —** Отдельно выпущенный официальный `Qwen3-Coder-480B-A35B-Base` в проверенных official card, repository tree и поиске Hugging Face не идентифицирован. Прямой upstream E-01 поэтому является Instruct checkpoint.

**VERIFIED FACT —** Official API evidence для закреплённой revision сообщает safetensors BF16 parameter count `480154875392`, `usedStorage=960313541352`, содержит `LICENSE` в file list и metadata `apache-2.0`.

**RISK —** Model card округляет total parameter count до 480B; точное API safetensors значение — `480154875392`. `usedStorage` является repository storage metadata, а не SHA-256, не доказательством полноты локальной загрузки и не заменой shard manifest. Memory plan требует shard-index audit и фактического H200 load/profile.

### Лицензионный caveat

**VERIFIED FACT —** API/card metadata на дату проверки указывала `license: apache-2.0`; API file list содержал `LICENSE`, доступный по <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/blob/9d90cf8fca1bf7b7acca42d3fc9ae694a2194069/LICENSE>.

**RISK —** Metadata `apache-2.0` не заменяет pinned license text и required notices. До скачивания весов, обучения, внутреннего распространения или выпуска derivative юридический владелец должен проверить применимость лицензии к exact revision и архивировать её вместе с notices.

**EXPERIMENT REQUIRED —** License preflight должен повторно проверить pinned file tree/API и сохранить HTTP evidence. Изменение upstream после 2026-07-13 не должно молча менять юридическую запись уже выполненного run.

### Политика адаптации

**ENGINEERING HYPOTHESIS —** Broad CPT исключён по умолчанию, потому что foundation уже post-trained: такой run может стереть instruction/tool alignment.

**ENGINEERING HYPOTHESIS —** Канонический lineage: `S0 → A1 → M1 → A2 → M2 → A3 → M3 → A4 → M4 → FP8`; train adapters сохраняются, каждый `M1..M4` создаётся отдельным BF16 merge job, FP8 — только serving derivative после parity.

**ENGINEERING HYPOTHESIS —** Internal MoE router и experts заморожены на начальных стадиях. Selective adaptation требует отдельного ablation gate.

**EXPERIMENT REQUIRED —** Каждый BF16 merge проходит integrity и regression gates. FP8 derivative допускается к serving только после parity с BF16 M4.

## 2. Историческая альтернативная ветвь

**VERIFIED FACT —** `Qwen/Qwen3-Coder-Next-Base` 80B/3B был прежним design choice, но больше не является foundation E-01.

**ENGINEERING HYPOTHESIS —** 80B/3B checkpoint может сохраняться только как исторически отвергнутая или отдельная alternative research branch; результаты этой ветви нельзя смешивать с lineage E-01.

**RISK —** Документы, configs или artifacts, которые всё ещё называют 80B/3B checkpoint E-01 foundation, являются stale и не санкционируют training run.

## 3. NVIDIA H200

Официальные URL:

- **VERIFIED FACT —** NVIDIA H200 product/specification page: <https://www.nvidia.com/en-us/data-center/h200/>
- **VERIFIED FACT —** NVIDIA H200 datasheet доступен через ссылку `Datasheet` на официальной product page; конкретный CDN URL не закрепляется, потому что NVIDIA может его менять.

**VERIFIED FACT —** Официальная NVIDIA page указывает для H200 SXM 141 GB HBM3e, memory bandwidth 4.8 TB/s, NVLink 900 GB/s, form factor SXM и HGX server options с 4 или 8 GPU.

**VERIFIED FACT —** Официальная NVIDIA page маркирует часть спецификаций как preliminary и subject to change.

**RISK —** Product specifications не доказывают effective training throughput LÆTEX. Memory fit, MFU, communication overhead и checkpoint time должны измеряться на фактическом RunPod cluster.

## 4. RunPod H200 infrastructure

### GPU и Instant Clusters

- **VERIFIED FACT —** GPU types: <https://docs.runpod.io/references/gpu-types>
- **VERIFIED FACT —** Instant Clusters overview: <https://docs.runpod.io/instant-clusters>
- **VERIFIED FACT —** Instant Clusters configuration/NCCL: <https://docs.runpod.io/instant-clusters/configuration>
- **VERIFIED FACT —** Slurm Clusters: <https://docs.runpod.io/instant-clusters/slurm-clusters>

**VERIFIED FACT —** RunPod GPU types page на дату проверки перечисляла `NVIDIA H200` / `H200 SXM` с 141 GB и pool `HOPPER_141`.

**VERIFIED FACT —** Instant Clusters overview указывал для H200 3200 Gbps и 2–8 nodes, то есть 16–64 GPUs; кластеры больше 8 nodes требуют обращения в sales.

**VERIFIED FACT —** Configuration page разделяет management interface `eth0` и high-bandwidth interfaces `ens1`–`ens8`, задаёт cluster environment variables и требует направлять NCCL на internal interface, пример: `NCCL_SOCKET_IFNAME=ens1`.

**RISK —** Термин `3200 Gbps` в документации RunPod — заявленный aggregate network figure, а не измеренная effective NCCL bandwidth. Нельзя автоматически приравнивать его к гарантированному InfiniBand payload throughput.

**EXPERIMENT REQUIRED —** Cluster acceptance test обязан записать SKU, node count, GPU topology, NCCL version, selected interfaces, all-reduce bandwidth, packet/error counters и стабильность минимум на representative duration до training run.

### Network Volumes

- **VERIFIED FACT —** Network Volumes: <https://docs.runpod.io/storage/network-volumes>
- **VERIFIED FACT —** Storage types: <https://docs.runpod.io/pods/storage/types>

**VERIFIED FACT —** RunPod документирует Network Volumes как persistent storage, независимое от compute; для Instant Clusters volume подключается при создании и монтируется на `/workspace` на каждом node.

**VERIFIED FACT —** Документация указывает standard и high-performance tiers, а также S3-compatible API для загрузки данных без запуска compute.

**RISK —** Network Volume не заменяет immutable object storage policy и backup. Документация предупреждает о риске data corruption при конкурентной записи в один volume; training artifacts требуют single-writer/atomic publish protocol.

**EXPERIMENT REQUIRED —** До масштабного run измеряются sustained read throughput для shards/datasets, write throughput checkpoint, metadata latency, concurrent-reader behavior и recovery из snapshot/replica.

## 5. Правила использования источников

**VERIFIED FACT —** Дата этой проверки — 2026-07-13. Это timestamp аудита, а не гарантия неизменности внешних страниц.

**ENGINEERING HYPOTHESIS —** Для каждого training/evaluation run registry должен хранить: URL, exact revision, retrieval timestamp, hashes скачанных файлов, model/config snapshots, license/notices snapshot и operator identity.

**RISK —** `main`, marketing pages, pricing и availability изменяемы. Они не могут быть единственным reproducibility anchor.

**RISK —** Benchmark numbers на upstream cards принадлежат upstream evaluation context. Они не переносятся на LÆTEX после post-training и не должны цитироваться как результаты LÆTEX.

**EXPERIMENT REQUIRED —** Перед release source audit повторяет все URL, сравнивает revisions/configs/licenses и создаёт signed source manifest.

## 6. Что не верифицировано этим документом

**VERIFIED FACT —** Не верифицированы: доступная RunPod quota, текущая цена, фактическая H200 topology конкретного заказа, sustained inter-node bandwidth, storage SLA, training wall-clock, inference latency, model quality и LÆTEX benchmark results.

**ENGINEERING HYPOTHESIS —** Эти данные должны появляться только как artifacts конкретных procurement, preflight, training и evaluation runs.

**RISK —** Любое числовое обещание качества, latency, throughput или стоимости без таких artifacts считается неподтверждённым.
