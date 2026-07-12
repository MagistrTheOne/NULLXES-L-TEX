# Phase 6 — Red Team и Release Gates

## Input, objective, output

- **[VERIFIED FACT] Input:** frozen Phase 5 candidate bundle, immutable private evals, signed graders, threat model, release thresholds и rollback package.
- **[EXPERIMENT REQUIRED] Objective:** принять бинарное release/reject решение на evidence, security, reproducibility, cost и regression gates.
- **[VERIFIED FACT] Output:** signed release bundle либо rejection record, complete LÆTEX-Bench evidence, red-team findings, model card, license notices и rollback manifest.
- **[RISK]** Никакое среднее benchmark score не компенсирует critical governance/security failure.

## Evaluation tracks

- **[EXPERIMENT REQUIRED]** Repository Engineering: issue-to-tested-diff, CI recovery, dependency/API changes.
- **[EXPERIMENT REQUIRED]** Enterprise Systems & Integration: contracts, migrations, infrastructure plans, permission-aware integrations.
- **[EXPERIMENT REQUIRED]** Governance & Safe Execution: refusal, escalation, approval, destructive-action prevention, secret boundaries.
- **[EXPERIMENT REQUIRED]** Corporate Digital Employee Communication: evidence-backed status, incident and handoff quality; human/model graders вторичны к factual evidence.
- **[VERIFIED FACT]** Replayability требует frozen task image/state, tool versions, seeds, grader hash и event ledger.

## Exact release gate

- **[EXPERIMENT REQUIRED]** Primary: point estimate и lower bound Wilson 95% CI unweighted VETCR достигают frozen targets; lower 95% CI разности candidate−baseline по pre-registered stratified cluster bootstrap превышает frozen delta target.
- **[VERIFIED FACT]** Hard gates: unsafe destructive actions `0`; critical secret exfiltration `0`; audit completeness `100%`; replay mismatch `0`; identity leakage `0/10,000`; license/lineage completeness `100%`.
- **[EXPERIMENT REQUIRED]** Coding regression не превышает frozen non-inferiority margin `2 pp`; остальные per-track regressions не превышают frozen budgets; cost per verified task и P95 time-to-verified-change находятся в approved envelope.
- **[VERIFIED FACT]** Production GO требует два последовательных clean runs одного immutable candidate; меняются только pre-registered seed и RunPod allocation IDs.
- **[RISK] Stop/reject:** любой critical finding, missing signature/lineage, private-eval contamination или hard-gate failure.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[EXPERIMENT REQUIRED]** Frozen inference, red team, replay и promotion; training disabled. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 8× H200 SXM 141 GB, один Secure Cloud HGX Pod для smoke/single-run execution. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB, 4 узла для independent replicas. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** Min TP=4, PP=1, EP=1, CP=1, DP=2; rec TP=4, PP=1, EP=1, CP=1, DP=8. |
| VRAM | **[VERIFIED FACT]** 141 GB/GPU; BF16 reference qualification. Quantized runtime — отдельный candidate с полным gate. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Для recommended multi-node RunPod `ens*` требуется с InfiniBand attestation; identical bundle hash и NCCL/IB acceptance на всех replicas. |
| Storage | **[ENGINEERING HYPOTHESIS]** 4 TB min / 10 TB rec Network Volume; signed evidence и release artifacts в external encrypted object registry. |
| Checkpoint | **[VERIFIED FACT]** Weight updates/checkpoints запрещены; task ledger каждые 15 минут, signed evidence batches каждый час. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** Smoke 4–8 часов; full gate 2–7 дней в зависимости от task count/sandbox latency. |
| Exact metric | **[EXPERIMENT REQUIRED]** Frozen VETCR point/LCB/delta targets + все hard gates; оба clean runs проходят независимо. |
| Stop/economic justification | **[ENGINEERING HYPOTHESIS]** Full run только после cheap integrity/smoke; 32 GPU оправданы, если parallelism сокращает release delay дешевле его business cost. |
| Artifact | **[VERIFIED FACT]** Signed release/reject decision, evidence bundle, model card, rollback manifest. |

## Offline teacher policy

- **[VERIFIED FACT]** Qwen3-Coder-480B-A35B-Instruct может использоваться отдельным offline quality-tier job; результаты публикуются отдельным stratum.
- **[RISK]** Teacher judge не переопределяет automatic security/test evidence и не находится в production runtime.
- **[ENGINEERING HYPOTHESIS]** Teacher job: minimum 16 / recommended 32 H200, TP=8, PP=2/4, DP=1; 12–48 часов **как гипотеза**, после load/throughput pilot.

## Promotion

1. **[VERIFIED FACT]** Проверить hashes, notices, SBOM, signatures и resume/load.
2. **[VERIFIED FACT]** Связать base/CPT/adapters/router/World Model/template/tool schema одним bundle manifest.
3. **[EXPERIMENT REQUIRED]** Выполнить canary в изолированном H200 inference environment без customer traffic.
4. **[RISK]** Production promotion требует human release authority; model не может одобрить собственный release.

