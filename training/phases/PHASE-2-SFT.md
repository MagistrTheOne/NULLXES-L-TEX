# Phase 2 — Supervised Fine-Tuning

## Input, objective, output

- **[VERIFIED FACT] Input:** accepted CPT checkpoint, unchanged tokenizer, LÆTEX chat template/tool grammar/response contract, verified SFT examples и protected replay set.
- **[ENGINEERING HYPOTHESIS] Objective:** записать LÆTEX identity, enterprise action behavior, evidence discipline, tool recovery и escalation policy.
- **[VERIFIED FACT] Output:** versioned adapter/trainable-state bundle, chat template, tool schema, identity report и task-level evidence.
- **[RISK]** Generic synthetic conversations без executable evidence размоют coding behavior и не должны доминировать.

## Training recipe

- **[ENGINEERING HYPOTHESIS]** Default — BF16 LoRA/domain adapters на projections/shared components; QLoRA запрещена до hybrid-MoE kernel/quality ablation.
- **[ENGINEERING HYPOTHESIS]** Initial target — 180k–300k verified examples; общий ActionWorld target отдельно включает 60k–120k executable trajectories и 20k–60k failure/recovery trajectories.
- **[VERIFIED FACT]** Every tool trajectory содержит initial state hash, action, observed delta, tests/policy evidence и final status.
- **[ENGINEERING HYPOTHESIS]** Mix: construction, architecture, integrations, DevOps/SRE, security, QA, communication, governance плюс 20–30% protected coding replay.
- **[RISK]** Teacher-generated examples допускаются только offline и проходят executable/human quality gate.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Gate:** VETCR `>=10% relative` к CPT; tool-call schema validity `>=99.5%`; identity leakage `0/10,000`; protected coding regression `<=2 pp`; evidence completeness `>=98%`.
- **[RISK] Stop:** identity leakage в release-candidate eval, validation deterioration два раза, schema validity <99%, или coding regression >2 pp.
- **[ENGINEERING HYPOTHESIS]** Экономический gate: accepted-example rate >=90%, а one-epoch pilot показывает положительный VETCR slope.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[ENGINEERING HYPOTHESIS]** Adapter/selective SFT 80B MoE backbone в BF16. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 8× H200 SXM 141 GB, один Secure Cloud HGX Pod для ограниченного adapter run. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB, 4 узла для ablations/throughput. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** Min TP=2, PP=1, EP=4, CP=1, DP=4; rec TP=2, PP=1, EP=8, CP=1, DP=16. |
| VRAM | **[VERIFIED FACT]** 1,128/4,512 GB aggregate HBM; base weights sharded, adapters/optimizer отдельно; activation checkpointing по measured need. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Для recommended multi-node RunPod `ens*` должен быть attested как InfiniBand; NCCL/IB и dataloader acceptance обязательны. |
| Storage | **[ENGINEERING HYPOTHESIS]** 4 TB min / 8 TB rec Network Volume; encrypted object store хранит immutable examples и release candidates. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** Каждые 500 steps или 2 часа; last-3, epoch-end, metric-best; resume test до promotion. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 4–10 дней на 8 H200 или 1–4 дня на 32 H200, включая periodic eval. |
| Exact metric | **[EXPERIMENT REQUIRED]** VETCR +10% relative, identity 0/10k, schema >=99.5%, regression <=2 pp. |
| Stop/economic justification | **[RISK]** Не масштабировать, если additional verified data улучшает VETCR дешевле GPU scaling или если pilot slope нулевой. |
| Artifact | **[VERIFIED FACT]** Adapter bundle + template/schema + identity/capability reports. |

## Identity controls

- **[VERIFIED FACT]** User-facing identity — LÆTEX; internal model card сохраняет происхождение и license notices.
- **[RISK]** Архитектурное происхождение и inherited representations не «стираются»; запрещено утверждать pretraining from zero.
- **[EXPERIMENT REQUIRED]** Проверить self-identification, indirect extraction, multilingual prompts, role conflicts, tool error paths и long-context identity drift.

