# Phase 6 — BF16 Release и FP8 parity

## Input, objective, output

- **[VERIFIED FACT] Input:** frozen `M4` BF16 master, independently accepted Phase 5 auxiliaries, immutable evals, signed graders, threat model и rollback package.
- **[EXPERIMENT REQUIRED] Objective:** принять бинарное release/reject решение на evidence, security, reproducibility, cost и regression gates.
- **[VERIFIED FACT] Output:** signed BF16 release/rejection plus optional separately signed FP8 export after parity.
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
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** BF16 16× H200; 8 физически тесны для ~960 GB weights плюс runtime overhead. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** BF16 32× H200; BF16→FP8 conversion/export и parity minimum 16 / recommended 32; final FP8 serving minimum 8 только после fit/parity. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** BF16 и FP8 conversion 16: TP8/PP2/CP1/DP1/EP1; 32: TP8/PP2/CP1/DP2/EP1. Final parity-approved FP8 serving 8: TP8/PP1/DP1; 8-GPU serving не выполняет conversion. |
| VRAM | **[ENGINEERING HYPOTHESIS]** BF16 source of truth; FP8 is a derived inference export, never training/merge parent. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Для recommended multi-node RunPod `ens*` требуется с InfiniBand attestation; identical bundle hash и NCCL/IB acceptance на всех replicas. |
| Storage | **[ENGINEERING HYPOTHESIS]** 4 TB min / 10 TB rec Network Volume; signed evidence и release artifacts в external encrypted object registry. |
| Checkpoint | **[VERIFIED FACT]** Training/merge disabled; retain `M4`, FP8 export, conversion manifest, ledger and signed evidence. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** Smoke 4–8 часов; BF16 gate 2–7 дней; FP8 parity ещё 1–3 дня. |
| Exact metric | **[EXPERIMENT REQUIRED]** Frozen VETCR point/LCB/delta targets + все hard gates; оба clean runs проходят независимо. |
| Stop/economic justification | **[ENGINEERING HYPOTHESIS]** Full run только после cheap integrity/smoke; 32 GPU оправданы, если parallelism сокращает release delay дешевле его business cost. |
| Artifact | **[VERIFIED FACT]** Signed release/reject decision, evidence bundle, model card, rollback manifest. |

## Critic policy

- **[VERIFIED FACT]** Default critic: none. `Qwen3-Coder-480B-A35B-Instruct` — foundation parent, не teacher.
- **[RISK]** Отдельный critic требует approval, отдельный checkpoint/lineage/budget и отдельный reporting stratum; automatic evidence остаётся authoritative.

## Promotion

1. **[VERIFIED FACT]** Проверить hashes, notices, SBOM, signatures и resume/load.
2. **[VERIFIED FACT]** Связать полный `S0 → A1 → M1 → A2 → M2 → A3 → M3 → A4 → M4 → FP8`, auxiliaries, tokenizer/template/tool schema одним bundle manifest.
3. **[EXPERIMENT REQUIRED]** Выполнить canary в изолированном H200 inference environment без customer traffic.
4. **[RISK]** Production promotion требует human release authority; model не может одобрить собственный release.
5. **[VERIFIED FACT]** FP8 promotion не изменяет BF16 master pointer и отменяется при любом parity failure.

