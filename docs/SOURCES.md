# Официальные источники и pinning

> Проверено: 2026-07-13  
> Scope: foundation checkpoints, NVIDIA H200, RunPod H200 compute/network/storage  
> Правило: model card и config проверяются вместе; mutable `main` не заменяет закреплённый revision.

## 1. Foundation Base

### Закреплённый объект

**VERIFIED FACT —** Repo ID: `Qwen/Qwen3-Coder-Next-Base`.

**VERIFIED FACT —** Закреплённый revision/SHA: `1b6df59d5f75ab51edb9ad8cb3ea69c5d0aedd57`.

**VERIFIED FACT —** Hugging Face API на дату проверки возвращал этот SHA как текущий `sha`, а также `private=false`, `gated=false`, library `transformers`, tensor format `safetensors` и metadata tag `license:apache-2.0`.

Официальные URL:

- **VERIFIED FACT —** Model card: <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base>
- **VERIFIED FACT —** Pinned model card: <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/blob/1b6df59d5f75ab51edb9ad8cb3ea69c5d0aedd57/README.md>
- **VERIFIED FACT —** Pinned raw model card: <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/raw/1b6df59d5f75ab51edb9ad8cb3ea69c5d0aedd57/README.md>
- **VERIFIED FACT —** Config: <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/blob/main/config.json>
- **VERIFIED FACT —** Pinned raw config: <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/raw/1b6df59d5f75ab51edb9ad8cb3ea69c5d0aedd57/config.json>
- **VERIFIED FACT —** Repository API metadata: <https://huggingface.co/api/models/Qwen/Qwen3-Coder-Next-Base>
- **VERIFIED FACT —** File tree: <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/tree/1b6df59d5f75ab51edb9ad8cb3ea69c5d0aedd57>
- **VERIFIED FACT —** Upstream technical report linked from card: <https://github.com/QwenLM/Qwen3-Coder/blob/main/qwen3_coder_next_tech_report.pdf>

### Проверенные параметры Base

**VERIFIED FACT —** Model card указывает: causal language model, training stage `Pretraining`, 80B total parameters, 3B activated parameters, 79B non-embedding parameters, hidden size 2048, 48 layers и native context 262 144.

**VERIFIED FACT —** Model card описывает hybrid layout как `12 × (3 × (Gated DeltaNet → MoE) → 1 × (Gated Attention → MoE))`.

**VERIFIED FACT —** Model card/config указывают 512 experts, 10 experts per token и 1 shared expert; config задаёт `num_experts=512`, `num_experts_per_tok=10`, `shared_expert_intermediate_size=512`.

**VERIFIED FACT —** Config задаёт `Qwen3NextForCausalLM`, `model_type=qwen3_next`, `num_hidden_layers=48`, `hidden_size=2048`, `max_position_embeddings=262144`, BF16 и vocabulary size 151 936.

**RISK —** Число total/activated parameters берётся из официального model card и API metadata; `config.json` не содержит самостоятельного поля total parameter count. Для training memory plan нужны отдельная проверка shard index и фактическая загрузка на H200.

### Лицензионный caveat

**VERIFIED FACT —** API metadata и card metadata на дату проверки указывали `apache-2.0` и ссылку <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/blob/main/LICENSE>.

**VERIFIED FACT —** Файл `LICENSE` отсутствовал в API file list, а запрос pinned URL <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/resolve/1b6df59d5f75ab51edb9ad8cb3ea69c5d0aedd57/LICENSE> вернул HTTP 404 при проверке 2026-07-13.

**RISK —** Metadata `apache-2.0` не заменяет текст лицензии и required notices. До скачивания весов, обучения, внутреннего распространения или выпуска derivative юридический владелец должен получить официальный license text, проверить применимость к exact revision и архивировать его вместе с notices.

**EXPERIMENT REQUIRED —** License preflight должен повторно проверить pinned file tree/API и сохранить HTTP evidence. Изменение upstream после 2026-07-13 не должно молча менять юридическую запись уже выполненного run.

## 2. Heavy teacher / quality tier

**VERIFIED FACT —** Кандидат teacher: `Qwen/Qwen3-Coder-480B-A35B-Instruct`.

Официальные URL:

- **VERIFIED FACT —** Model card: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct>
- **VERIFIED FACT —** Config: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/blob/main/config.json>
- **VERIFIED FACT —** Raw config: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/raw/main/config.json>
- **VERIFIED FACT —** Repository API metadata: <https://huggingface.co/api/models/Qwen/Qwen3-Coder-480B-A35B-Instruct>
- **VERIFIED FACT —** File tree: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct/tree/main>

**VERIFIED FACT —** Model card указывает 480B total / 35B activated, 62 layers, GQA 96 Q / 8 KV heads, 160 experts, 8 activated experts и native context 262 144.

**VERIFIED FACT —** Config подтверждает `Qwen3MoeForCausalLM`, `model_type=qwen3_moe`, hidden size 6144, 62 layers, 160 experts, Top-8 и 262 144 positions.

**RISK —** Teacher URL использует mutable `main`, потому что в этом baseline закреплён только известный Base SHA. Teacher нельзя использовать в production generation run, пока его exact revision, license/notices, shard hashes и serving config не внесены в registry.

**EXPERIMENT REQUIRED —** Teacher остаётся кандидатом до измерения trajectory quality, verifier calibration, H200 throughput и cost per accepted example. Его upstream benchmark claims не являются результатами LÆTEX.

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
