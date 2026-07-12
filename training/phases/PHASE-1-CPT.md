# Phase 1 — Identity / Tool LoRA

> Compatibility filename only. Broad CPT disabled; этот файл не определяет CPT run.

## Canonical profiles and lineage position

- **[VERIFIED FACT]** Identity `A1`: [`../../infra/runpod/profiles/identity-lora.yaml`](../../infra/runpod/profiles/identity-lora.yaml).
- **[VERIFIED FACT]** Separate BF16 merge `M1`: [`../../infra/runpod/profiles/merge-m1.yaml`](../../infra/runpod/profiles/merge-m1.yaml).
- **[VERIFIED FACT]** Optional DAPT points only to disabled contract [`../../infra/runpod/profiles/cpt-disabled.yaml`](../../infra/runpod/profiles/cpt-disabled.yaml); broad CPT has no enabled profile in E-01.
- **[VERIFIED FACT]** Strict position: accepted `S0 → A1 → M1`; action `A2` cannot consume an unmerged adapter.
- **[RISK]** Missing, disabled, unsigned or hash-unpinned profile blocks the corresponding job. No run or gate pass is claimed here.

## Input, objective, output

- **[VERIFIED FACT] Input:** accepted Phase 0, immutable `S0` BF16 foundation/tokenizer, identity/tool contract examples, protected replay и lineage.
- **[ENGINEERING HYPOTHESIS] Objective:** записать LÆTEX identity, response contract и tool grammar BF16 LoRA без изменения base router/experts.
- **[VERIFIED FACT] Output contract:** retained `A1`, then BF16 merged `M1=S0+A1`, fresh-optimizer record, merge parity и identity/capability reports.
- **[RISK]** Tokenizer не меняется. Broad CPT disabled.

## Trainable scope и optional DAPT

- **[ENGINEERING HYPOTHESIS]** Default LoRA targets dense attention projections; upstream MoE router и 160 routed experts frozen.
- **[VERIFIED FACT]** Upstream config сообщает `shared_expert_intermediate_size: 0`; нельзя проектировать Stage 1 вокруг несуществующего shared expert.
- **[EXPERIMENT REQUIRED]** DAPT допускается только как отдельно approved ablation после явной замены disabled state в `cpt-disabled.yaml`, с отдельным budget, data gate и no-regression criterion; он не создаёт default master lineage.
- **[VERIFIED FACT]** Raw tenant data запрещены без explicit opt-in lineage.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Gate:** identity leakage `0/10,000`; tool-schema validity `>=99.5%`; protected coding regression `<=2 pp`; merge parity passes.
- **[RISK] Stop:** identity leakage, regression >2 pp twice, NaN/Inf или любое изменение router/expert weights.
- **[ENGINEERING HYPOTHESIS]** Scale gate: short-sequence pilot показывает positive identity/tool gain per dollar.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[ENGINEERING HYPOTHESIS]** BF16 identity/tool LoRA on direct 480B/35B foundation. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 16× H200 для 8–16K. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 для 8–16K; 64× для 32–64K. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** 16: TP8/PP2/CP1/DP1/EP1; 32: TP8/PP2/CP1/DP2/EP1; 64: TP8/PP2/CP2/DP2/EP1. |
| VRAM | **[ENGINEERING HYPOTHESIS]** BF16 foundation sharded; LoRA/optimizer separately sharded; activation checkpointing and CP measured before long context. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Inter-node allocation обязан иметь attested InfiniBand на RunPod `ens*`; 3200 Gbps marketing figure недостаточен. **[EXPERIMENT REQUIRED]** IB/NCCL all-to-all до загрузки corpus. |
| Storage | **[ENGINEERING HYPOTHESIS]** Network Volume working set; encrypted registry stores `S0/A1/M1` and manifests. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** Adapter/optimizer каждые 500 steps или 2 часа; retain `A1`; merge to `M1` only after resume/load gate. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 8–16K: 2–6 дней/16 или 1–3/32; 32–64K: 2–6/64 после pilot. |
| Exact metric | **[EXPERIMENT REQUIRED]** Identity 0/10k, schema >=99.5%, regression <=2 pp. |
| Stop/economic justification | **[RISK]** No scale without positive pilot; optional DAPT needs separate approval. |
| Artifact | **[VERIFIED FACT]** `A1`, `M1` BF16, merge lineage, identity/capability report. |

## Additional controls

- **[VERIFIED FACT]** Stage 1 optimizer fresh; его state не переносится через merge `M1`.
- **[VERIFIED FACT]** Merge parent/output — BF16. FP8 запрещён как parent.
- **[VERIFIED FACT]** `A1` training и `M1` merge — разные H200 jobs с разными canonical profile hashes; локальный merge запрещён.
- **[RISK]** Full-parameter 480B не E-01; `>=128 H200` обсуждается только после memory proof.

