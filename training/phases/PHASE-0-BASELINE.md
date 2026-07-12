# Phase 0 — Baseline direct 480B foundation

## Canonical profile and lineage position

- **[VERIFIED FACT]** Profile: [`../../infra/runpod/profiles/baseline.yaml`](../../infra/runpod/profiles/baseline.yaml).
- **[VERIFIED FACT]** Position: `S0` baseline must pass before identity `A1`; Phase 0 does not create a new weight checkpoint.
- **[RISK]** Missing, unsigned or hash-unpinned profile blocks execution. No run or result is claimed here.

## Input, objective, output

- **[VERIFIED FACT] Input:** immutable BF16 `Qwen/Qwen3-Coder-480B-A35B-Instruct` (`S0`), unchanged tokenizer/chat template hash, frozen LÆTEX-Bench, private holdouts и deterministic graders.
- **[EXPERIMENT REQUIRED] Objective:** измерить quality, latency, tool reliability, safety, identity leakage и cost до weight changes.
- **[VERIFIED FACT] Output:** signed baseline manifest, evidence, failure taxonomy, latency/cost distributions и contamination audit.
- **[RISK]** Это foundation/production candidate, не teacher. Model judge не заменяет executable grader.

## Procedure

1. **[VERIFIED FACT]** Зафиксировать checkpoint/tokenizer/image/dataset/grader hashes.
2. **[EXPERIMENT REQUIRED]** Прогнать четыре трека LÆTEX-Bench с одинаковыми retry/tool budgets.
3. **[EXPERIMENT REQUIRED]** Измерить cold/warm TTFT, time-to-verified-change, pass-to-pass, recovery after injected tool failures и cost per verified task.
4. **[EXPERIMENT REQUIRED]** Выполнить identity/adversarial baseline, чтобы размер overwrite измерялся, а не предполагался.
5. **[VERIFIED FACT]** Replay 10% stratified tasks должен воспроизводить grader outcome.

## Exact success metric и stop condition

- **[VERIFIED FACT] Primary metric:** `VETCR = verified completed tasks / all eligible attempted tasks`; skipped/timeouts считаются failures.
- **[EXPERIMENT REQUIRED] Gate:** 100% task-attempt accounting, replay mismatch `0`, missing evidence `0`, contamination findings resolved; unweighted VETCR имеет Wilson 95% CI, а comparison plan — pre-registered stratified cluster bootstrap по task families.
- **[RISK] Stop:** checksum mismatch, grader nondeterminism вне frozen tolerance, утечка private eval в training namespace или любое изменение weights.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[EXPERIMENT REQUIRED]** Воспроизводимая baseline inference/evaluation без weight updates. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 16× H200 SXM 141 GB, два HGX-узла после BF16 load/memory proof. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB, четыре узла, две replicas. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** Min world=16: TP=8, PP=2, CP=1, DP=1, EP=1; rec world=32: TP=8, PP=2, CP=1, DP=2, EP=1. |
| VRAM | **[ENGINEERING HYPOTHESIS]** BF16 weights ≈960 GB before runtime overhead; 16 H200 is minimum, 32 adds replica/headroom. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch внутри узла. **[RISK]** Для recommended multi-node требуется attested InfiniBand на RunPod `ens*`; публичные 3200 Gbps сами по себе этого не доказывают. |
| Storage | **[VERIFIED FACT]** `/workspace` Network Volume для working set; external encrypted object store для frozen inputs/evidence. |
| Checkpoint | **[VERIFIED FACT]** `S0` immutable; weight checkpoints не создаются; task ledger/evidence каждые 15 минут. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** 12–36 часов для первого полного suite; уточнить после 100-task pilot. |
| Exact metric | **[VERIFIED FACT]** VETCR, Wilson 95% CI для unweighted rate, replay mismatch=0, audit completeness=100%. |
| Stop/economic justification | **[ENGINEERING HYPOTHESIS]** Full run оправдан только после frozen graders; 32 GPU — если wall-clock saving дешевле задержки решения. |
| Artifact | **[VERIFIED FACT]** `baseline-results`, replay bundle, cost/latency manifest, gate decision. |

## Risks

- **[RISK]** Small private suite даст широкий confidence interval; увеличить task count, а не скрывать uncertainty.
- **[RISK]** Long-context prompts могут превратить benchmark в I/O test; отдельно публиковать retrieval/context strata.
- **[RISK]** RunPod capacity/topology variance требует cluster acceptance report для каждого allocation.
- **[VERIFIED FACT]** Локальные model workloads запрещены; Phase 0 выполняется только на H200 inference/evaluation allocation.

