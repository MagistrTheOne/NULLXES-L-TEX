# RunPod-only compute architecture для LÆTEX E-01

## 1. Foundation decision

- **[VERIFIED FACT]** Единственный foundation и production candidate: `Qwen/Qwen3-Coder-480B-A35B-Instruct`, 480B total / 35B activated, 62 layers, 160 experts, Top-8, native 262,144 context, BF16 upstream weights.
- **[VERIFIED FACT]** Разделение 80B student / 480B teacher удалено. Тот же 480B checkpoint нельзя называть teacher: он является родителем LÆTEX.
- **[RISK]** Отдельный critic допускается только отдельным архитектурным и бюджетным approval, с собственным checkpoint ID и lineage. По умолчанию critic отсутствует.
- **[ENGINEERING HYPOTHESIS]** E-01 обучает LoRA/adapters и последовательно сливает их в BF16 masters; full-parameter 480B tuning не входит в E-01.
- **[RISK]** Full-parameter 480B training потребует не менее 128 H200 и допускается только после optimizer/checkpoint memory proof; это нижняя гипотеза, не утверждение feasibility.

## 2. Изолированные compute-контуры

### H200 training

- **[VERIFIED FACT]** Только NVIDIA H200 SXM 141 GB, homogeneous HGX nodes по 8 GPU, NVLink/NVSwitch внутри узла и InfiniBand между узлами.
- **[ENGINEERING HYPOTHESIS]** Baseline и 8–16K LoRA: minimum 16 / recommended 32 H200. Для 32–64K LoRA: recommended 64. Preference: 32/64. GRPO: 64/128.
- **[RISK]** Стандартный RunPod Instant Cluster ограничен 16–64 GPU; 128 H200 для GRPO требует заранее подтверждённой capacity через RunPod sales.
- **[ENGINEERING HYPOTHESIS]** Pinned OCI image + Megatron-Core/Megatron-LM + Transformer Engine; DeepSpeed только после phase parity.

### H200 inference/evaluation

- **[ENGINEERING HYPOTHESIS]** BF16 480B weights занимают около 960 GB до runtime overhead. Поэтому BF16 minimum 16 / recommended 32 H200; 8 H200 физически слишком тесны для release qualification.
- **[ENGINEERING HYPOTHESIS]** FP8 candidate: minimum 8 / recommended 16 H200 только после BF16-to-FP8 load, numerical и LÆTEX-Bench parity.
- **[VERIFIED FACT]** Training, rollout serving и release evaluation используют раздельные allocations.

### Local control plane

- **[VERIFIED FACT]** Локально разрешены Git, профили, job submission, агрегированные метрики и лёгкие unit tests без весов.
- **[VERIFIED FACT]** Локальные inference, training, LoRA, merge, CPT/DAPT, RL и generation запрещены.

## 3. Staged BF16 lineage

| ID | Родитель | Изменение | Результат |
|---|---|---|---|
| `U0` | upstream | Immutable BF16 foundation | Source master |
| `M1` | `U0` | Retained `A1` identity/tool LoRA, затем BF16 merge | Stage 1 master |
| `M2` | `M1` | Retained `A2` Enterprise Action SFT LoRA, затем BF16 merge | Stage 2 master |
| `M3` | `M2` | Retained `A3` DPO/IPO LoRA, затем BF16 merge | Stage 3 master |
| `M4` | `M3` | Retained `A4` GRPO LoRA, затем BF16 merge | Release BF16 master |

- **[VERIFIED FACT]** Каждый `A1..A4`, его pre-merge parent, merge manifest и post-merge eval сохраняются.
- **[ENGINEERING HYPOTHESIS]** Merge выполняется BF16-совместимым детерминированным job, затем load test и полный protected regression gate.
- **[VERIFIED FACT]** Каждая стадия начинает новый optimizer/scheduler; optimizer state не переносится через merge boundary.
- **[VERIFIED FACT]** FP8 — только производный inference export от `M4`; FP8 никогда не является training или merge parent.
- **[RISK]** Base MoE router и 160 routed experts frozen в Phases 1–4. Их разморозка требует отдельного ablation и не является E-01 default.

## 4. Storage и checkpoints

| Уровень | Назначение | Политика |
|---|---|---|
| `/workspace` Network Volume | active shards, adapters, rollout queues, staging checkpoints | Working set, не source of truth |
| Node-local scratch | cache/compilation/transient artifacts | Ephemeral, checksum-bound |
| External encrypted object store | `U0`, `A1..A4`, `M1..M4`, optimizer states, datasets, evidence | Versioned immutable registry |

- **[ENGINEERING HYPOTHESIS]** Один run — один write namespace; promotion выполняет единственный registry writer после checksum и resume/load test.
- **[RISK]** Merge без adapter retention, parent hash, tokenizer/template hash или post-merge parity считается недействительным.

## 5. Network acceptance

- **[RISK]** Публичное «до 3200 Gbps» и наличие `ens*` не доказывают InfiniBand конкретного allocation.
- **[VERIFIED FACT]** Перед каждым run нужны письменная provider attestation InfiniBand, topology inventory, NCCL test, no-`eth0` fallback, 141 GB HBM/rank и zero XID/ECC.
- **[EXPERIMENT REQUIRED]** Для training дополнительно: distributed loss/gradient parity; для GRPO: rollout/update sync и sandbox containment; для release: identical bundle hashes.

## 6. Profile contract

- **[VERIFIED FACT]** Все `infra/runpod/profiles/*.yaml` используют `laetex.runpod.profile/v2` и одинаковые top-level keys.
- **[VERIFIED FACT]** `world_size = TP × PP × CP × DP`. `EP` не умножается второй раз; его group semantics проходят отдельную Megatron validation.
- **[ENGINEERING HYPOTHESIS]** EP=1 в E-01 Phases 0–4, потому что upstream router/experts frozen. Top-2 domain-adapter router Phase 5 — иной механизм, не base-MoE EP.
- **[VERIFIED FACT]** Каждый профиль задаёт network attestation, working/durable storage, checkpoint input/output/cadence/retention, wall-clock как hypothesis, exact metric и economic gate.

## 7. Security и tenancy

- **[VERIFIED FACT]** Только RunPod Secure Cloud; Community Cloud запрещён.
- **[ENGINEERING HYPOTHESIS]** Раздельные projects, volumes, object prefixes, KMS keys и short-lived identities для `dev/eval/train/release`.
- **[RISK]** Tenant data не попадают в общий corpus без explicit opt-in lineage; logs, crash dumps и telemetry проверяются на source/secrets leakage.

## 8. Source snapshot

- **[VERIFIED FACT]** Model card и `config.json` проверены 2026-07-13: 480B/35B, 62 layers, 96Q/8KV, 160 experts, 8 active, BF16, 262,144 context; config указывает `shared_expert_intermediate_size: 0`.
- **[RISK]** License/notices и deployment compatibility должны фиксироваться отдельным release artifact; параметры и RunPod limits перепроверяются перед reservation.

