# Phase 1 — Continued Pretraining

## Input, objective, output

- **[VERIFIED FACT] Input:** Phase 0 gate, immutable base checkpoint/tokenizer, licensed and deduplicated LÆTEX Corpus shards, holdouts, lineage manifests.
- **[ENGINEERING HYPOTHESIS] Objective:** адаптировать representations к enterprise code/system/action language без потери базовой coding capability.
- **[VERIFIED FACT] Output:** resumable CPT checkpoint, optimizer/RNG/data-cursor state, data lineage, learning curves и protected-capability report.
- **[RISK]** Tokenizer не меняется: смена нарушит embedding compatibility и превратит CPT в существенно более рискованное обучение.

## Trainable scope и data

- **[EXPERIMENT REQUIRED]** Сравнить: (A) attention/DeltaNet projections + norms + shared experts; (B) A + router; (C) controlled broader tune.
- **[RISK]** Router update может вызвать expert collapse; router остается frozen, если B не даёт statistically useful VETCR gain.
- **[ENGINEERING HYPOTHESIS]** Начальный corpus target: 20–50B high-quality tokens; окончательный объём определяется scaling pilot, а не календарём.
- **[VERIFIED FACT]** Raw tenant data по умолчанию запрещены; opt-in records требуют tenant, license, consent, PII transform и revocation lineage.
- **[ENGINEERING HYPOTHESIS]** Replay mix включает upstream-compatible code/general tokens для снижения catastrophic forgetting.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Gate:** relative held-out enterprise-code NLL improves `>=3%`; VETCR regression `<=2 pp`; protected coding pass rate regression `<=2 pp`; identity/tool SFT не оценивается как цель CPT.
- **[RISK] Stop:** NaN/Inf, unrecoverable loss spike, protected regression >2 pp на двух evals, либо >30% experts имеют <5% normalized utilization на двух windows.
- **[ENGINEERING HYPOTHESIS]** Экономический gate: 1% token pilot должен прогнозировать cost per incremental VETCR point ниже approved threshold; threshold фиксируется finance owner до run.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[ENGINEERING HYPOTHESIS]** Selective/full-scope CPT 80B-total/3B-active MoE backbone. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB, 4 узла; только pilot/минимально жизнеспособный production run. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 64× H200 SXM 141 GB, 8 узлов. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** Min TP=2, PP=2, EP=8, CP=1, DP=8; rec TP=2, PP=2, EP=8, CP=2, DP=8. EP mapping требует Megatron dry-run. |
| VRAM | **[VERIFIED FACT]** 4,512/9,024 GB aggregate HBM; BF16 first. Optimizer/state sharding и activation checkpointing обязательны. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Inter-node allocation обязан иметь attested InfiniBand на RunPod `ens*`; 3200 Gbps marketing figure недостаточен. **[EXPERIMENT REQUIRED]** IB/NCCL all-to-all до загрузки corpus. |
| Storage | **[ENGINEERING HYPOTHESIS]** 8 TB min / 20 TB rec high-performance Network Volume working set; durable encrypted object registry отдельно. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** Distributed checkpoint каждые 250 steps или 2 часа; last-3 + daily + metric-best; каждый promoted checkpoint проходит resume test. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 20B tokens: 7–21 дней на 64 H200; диапазон нельзя считать benchmark до measured tokens/s. |
| Exact metric | **[EXPERIMENT REQUIRED]** NLL −3% relative при VETCR/protected regression <=2 pp. |
| Stop/economic justification | **[RISK]** Не запускать 20–50B tokens, если pilot slope не достигает frozen quality-per-dollar threshold. |
| Artifact | **[VERIFIED FACT]** CPT checkpoint + optimizer/resume state + lineage + regression report. |

## Additional controls

- **[EXPERIMENT REQUIRED]** BF16 proxy обязателен до FP8; FP8 принимается только при loss/gradient parity и equal-or-better throughput.
- **[RISK]** Network Volume throughput может ограничить dataloader; разрешён node-local read cache с checksum, но registry topology не меняется.
- **[RISK]** Full 80B optimizer state дорог и медленен в checkpointing; broader tune не разрешается без memory/throughput acceptance.

