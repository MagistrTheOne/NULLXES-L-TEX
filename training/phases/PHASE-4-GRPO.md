# Phase 4 — GRPO / Executable RL

## Input, objective, output

- **[VERIFIED FACT] Input:** accepted `M3` BF16, isolated executable sandboxes, immutable tasks, deterministic tests, policy engine, failure injections и reward specification.
- **[ENGINEERING HYPOTHESIS] Objective:** повысить verified completion и recovery после tool failures, оптимизируя observed outcome, а не правдоподобный текст.
- **[VERIFIED FACT] Output:** retained `A4`, BF16 `M4=M3+A4`, fresh optimizer record, replayable trajectories, reward/security и merge parity.
- **[RISK]** Эта фаза условна: если additional verified SFT даёт такой же gain дешевле и стабильнее, GRPO — NO-GO.

## Reward и containment

- **[VERIFIED FACT]** Positive reward требует passed tests/policy checks, expected state delta и complete evidence.
- **[ENGINEERING HYPOTHESIS]** Reward components: verified task completion, partial test progress, recovery, minimal reversible changes, evidence completeness; hard penalties за policy violation и unapproved side effects.
- **[RISK]** Model-based reward не может единолично подтверждать completion.
- **[VERIFIED FACT]** Sandboxes не имеют production credentials, customer networks или write access вне task namespace.
- **[EXPERIMENT REQUIRED]** Проверить reward replay determinism и adversarial reward hacking до policy updates.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Gate:** VETCR `>=8% relative` к preference model; failure-recovery success `>=60%`; unsafe destructive side effects `0`; protected coding regression `<=2 pp`; positive lower bound 95% CI на gain.
- **[RISK] Stop:** любой uncontained destructive effect, подтверждённый reward hack на 2 разных tasks, KL/capability bound violated дважды или rollout evidence loss.
- **[ENGINEERING HYPOTHESIS]** Экономический gate: 1,000-task pilot должен показать lower 95% CI >0 и projected cost per incremental verified task ниже frozen SFT alternative.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[EXPERIMENT REQUIRED]** Adapter-first GRPO с distributed rollouts и policy updates. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 64× H200 SXM 141 GB, 8 узлов. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 128× H200, 16 узлов; требует RunPod capacity/contact sales beyond standard 64. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** 64: TP8/PP2/CP2/DP2/EP1; 128: TP8/PP2/CP2/DP4/EP1. Rollout/update ranks sum exactly to world size. |
| VRAM | **[ENGINEERING HYPOTHESIS]** 9,024/18,048 GB aggregate HBM; policy/optimizer/rollout residency подтверждается memory proof. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** RunPod `ens*` требуется с InfiniBand attestation; policy sync/rollout queues изолированы, NCCL/IB acceptance обязателен. |
| Storage | **[ENGINEERING HYPOTHESIS]** 8 TB min / 20 TB rec Network Volume; object store хранит только accepted/required audit trajectories и checkpoints. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** `A4` + fresh optimizer/RNG/rollout cursor каждые 100 updates/60 минут; retain `M3/A4/M4`. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 64-H200 pilot 3–7 дней; 128-H200 gated run 7–21 день. |
| Exact metric | **[EXPERIMENT REQUIRED]** VETCR +8% relative, recovery >=60%, unsafe effects=0, lower 95% CI >0. |
| Stop/economic justification | **[RISK]** Немедленный stop при containment failure; scale только если pilot превосходит frozen SFT cost baseline. |
| Artifact | **[VERIFIED FACT]** `A4`, `M4` BF16, trajectory corpus, merge/reward/security reports, go/no-go. |

## Operational risks

- **[RISK]** Sandbox throughput, а не H200, может стать bottleneck; измерять GPU idle ratio и не покупать дополнительные GPU для скрытия orchestration defect.
- **[RISK]** Correlated rollouts уменьшают effective sample size; публиковать task-family clustered confidence intervals.
- **[EXPERIMENT REQUIRED]** Failure injection должен включать timeout, malformed tool output, permission denial, stale state и partial test failure.
- **[VERIFIED FACT]** Base router/experts remain frozen; Stage 4 optimizer is fresh; FP8 never parents `M4`.

