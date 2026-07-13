# Архитектура LÆTEX: source of truth

> **VERIFIED FACT —** Версия: 0.2.
> **VERIFIED FACT —** Дата решения: 2026-07-13.
> **VERIFIED FACT —** Статус: independent E-01 baseline; не доказательство реализованной системы.

## Positioning and decision

- **ENGINEERING HYPOTHESIS:** LÆTEX is an Enterprise Action Model that plans and executes typed actions against authorized enterprise state and returns verified artifacts, evidence, risks and audit records.
- **VERIFIED FACT:** ADR-0007 replaces the derivative foundation with independent from-scratch E-01.
- **VERIFIED FACT:** E-01 has no external weight parent, checkpoint initialization or inherited tokenizer.
- **VERIFIED FACT:** Qwen is external benchmark and optional offline synthetic teacher only under ADR-0009.
- **RISK:** From-scratch status does not prove originality of every architectural idea, model quality, safety, schedule or economic viability.

## Foundation target

| Component | Decision state |
|---|---|
| Core | **ENGINEERING HYPOTHESIS:** decoder-only sparse MoE, 64 layers, `d_model=8192` |
| Attention | **ENGINEERING HYPOTHESIS:** GQA `64Q/8KV`, head dimension 128 |
| Hybrid pattern | **ENGINEERING HYPOTHESIS:** 7 local + 1 global; local window 16 384 |
| MoE | **ENGINEERING HYPOTHESIS:** 144 routed experts + 1 shared, Top-6, expert `d_ff=2048` |
| Tokenizer | **VERIFIED FACT:** custom; **ENGINEERING HYPOTHESIS:** vocabulary target 128K |
| Context | **ENGINEERING HYPOTHESIS:** target 262 144 through staged curriculum |
| Master | **VERIFIED FACT:** BF16 |
| Size | **EXPERIMENT REQUIRED:** `~478.9B total / ~34.4B active`, pending proxy validation |

- **EXPERIMENT REQUIRED:** Exact parameter accounting must pin MoE placement, shared-expert definition, embedding/output tying, norms, router parameters and attention projections.
- **RISK:** Hybrid attention kernels, Top-6 all-to-all and 262K training can dominate systems risk despite sparse active parameters.

## Physical boundaries

### Local control/documentation plane

- **VERIFIED FACT:** Local machine is limited to code, documentation, configs, orchestration, redacted metadata and lightweight tests without model weights.
- **VERIFIED FACT:** Local training, fine-tuning, RL, teacher generation and model inference are prohibited.

### H200 training plane

- **VERIFIED FACT:** All model workloads use homogeneous NVIDIA H200 HGX nodes with NVLink/NVSwitch intra-node.
- **VERIFIED FACT:** Multi-node jobs require provider-attested InfiniBand and successful NCCL acceptance.
- **ENGINEERING HYPOTHESIS:** Megatron-Core/DeepSpeed-equivalent distributed stack uses TP/PP/EP/CP/DP mapping selected by measured proxy behavior.
- **EXPERIMENT REQUIRED:** GPU count, topology, memory fit, MFU, storage throughput, checkpoint time and wall-clock remain run-specific evidence.

### H200 inference/evaluation plane

- **VERIFIED FACT:** Inference, evaluation and optional teacher generation use separate H200 pools and credentials.
- **RISK:** External teacher service cannot enter live runtime or authoritative policy decisions.

## Five planes

### 1. Foundation Plane

- **VERIFIED FACT:** Scratch lineage follows ADR-0010: `C0 → T0 → R0 → P0..Pn → G0 → PT0..PTn → B0 → SFT0 → PREF0 → RL0 → M0`.
- **VERIFIED FACT:** R0 is random initialization; B0 and M0 are immutable BF16 artifacts.
- **EXPERIMENT REQUIRED:** Proxies validate parameter count, optimization, routing, scale transfer, hybrid attention, recovery and H200 communication before G0.
- **RISK:** Any external checkpoint in weight-parent graph invalidates canonical lineage.

### 2. Adapter/Domain Routing Plane

- **ENGINEERING HYPOTHESIS:** Eight domain packs remain candidates: Code Construction, Systems Architecture, Integrations, DevOps/SRE, Security & Compliance, QA/Review, Enterprise Communication and Governance/Escalation.
- **ENGINEERING HYPOTHESIS:** Request-level router may select Top-2 domain packs plus shared Evidence/Policy behavior after base/post-training baselines exist.
- **VERIFIED FACT:** Request-level routing is distinct from token-level base MoE routing.
- **EXPERIMENT REQUIRED:** Adapter routing remains post-training experiment and is not part of foundation parameter estimate.

### 3. CodeWorld Plane

- **ENGINEERING HYPOTHESIS:** CodeWorld represents repository tree, symbols, dependencies, API contracts, Git/CI, issues, telemetry, ADR, ownership, secrets boundaries, policies and scopes.
- **ENGINEERING HYPOTHESIS:** Object store holds immutable blobs; graph/index holds relations; relational metadata holds versions/ACL; append-only ledger records events.
- **ENGINEERING HYPOTHESIS:** Model context receives only authorized task-relevant slices with version and provenance IDs.
- **RISK:** Writes invalidate affected state and block dependent actions until refresh; stale state cannot be silently treated as current.

### 4. Organizational World Model Plane

- **ENGINEERING HYPOTHESIS:** V0 is deterministic graph + event ledger + policy engine over typed state/action/observed-delta contracts.
- **ENGINEERING HYPOTHESIS:** Future V1 may learn transition/risk predictions after sufficient verified traces but cannot replace authoritative stores.
- **RISK:** Predicted state is not observed state and cannot update the ledger without tool evidence.

### 5. Execution and Verification Plane

- **ENGINEERING HYPOTHESIS:** Closed loop: Task → Plan → Read → Simulate → Execute in Sandbox → Test → Verify → Report → Update World State.
- **ENGINEERING HYPOTHESIS:** Tools are typed as read-only, simulated-write, controlled-write or privileged; each has permission, idempotency, timeout, rollback and evidence contracts.
- **VERIFIED FACT:** Irreversible/destructive action requires explicit human approval independent of model confidence.
- **EXPERIMENT REQUIRED:** Sandbox escape, credential leakage, prompt injection, confused-deputy and rollback paths require red-team evidence before release.

## Tokenizer, data and teacher boundaries

- **VERIFIED FACT:** ADR-0008 requires custom tokenizer freeze before pretraining.
- **VERIFIED FACT:** Raw tenant data is excluded from common training by default; explicit opt-in requires contractual and technical isolation plus lineage.
- **VERIFIED FACT:** ADR-0009 quarantines all Qwen teacher candidates from benchmark holdouts and model weight lineage.
- **RISK:** Synthetic teacher data can import identity, errors, unsafe tool behavior and contamination; executable verification is mandatory.

## Artifact and release contract

- **VERIFIED FACT:** Required provenance includes source/license/PII manifests, tokenizer hash, R0 recipe, code/container digest, seeds, H200 topology, configs, checkpoints, raw evals and rollback pointers.
- **EXPERIMENT REQUIRED:** Release requires frozen coding/tool/governance/safety gates, tenant-isolation tests, reproducible VETCR report and BF16-to-serving parity.
- **RISK:** Existing derivative-era files outside this decision wave may be stale and cannot authorize a run; ADR-0007/0008/0009/0010 and this document take precedence.
- **VERIFIED FACT:** Superseded Qwen-derivative documentation is preserved only under `docs/branches/HISTORICAL/qwen-derivative-e01/`.
