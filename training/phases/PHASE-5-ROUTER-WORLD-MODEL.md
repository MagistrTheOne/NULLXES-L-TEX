# Phase 5 — Adapter Router и Organizational World Model

## Canonical profile and lineage isolation

- **[VERIFIED FACT]** Auxiliary profile: [`../../infra/runpod/profiles/router-world-model.yaml`](../../infra/runpod/profiles/router-world-model.yaml).
- **[VERIFIED FACT]** Phase 5 is not a policy merge stage and cannot interrupt or reorder `M4 → FP8 parity/export → release eval`.
- **[RISK]** Missing, unsigned or hash-unpinned profile blocks auxiliary jobs. No run, trained router or World Model result is claimed here.

## Input, objective, output

- **[VERIFIED FACT] Input:** frozen `M4` BF16 policy, eight domain adapter packs, shared Evidence/Policy adapter, task/state metadata, traces и deterministic World Model V0.
- **[ENGINEERING HYPOTHESIS] Objective:** выбрать Top-2 domain adapters с audit trail и, условно, обучить compact 1.5–3B transition model, превосходящий V0.
- **[VERIFIED FACT] Output:** independent calibrated adapter router, route explanations, compatibility matrix и World Model V1 либо signed no-go; ничего не сливается в `M4`.
- **[RISK]** Adapter router — не base MoE router; их losses, expert IDs и audit semantics нельзя смешивать.
- **[VERIFIED FACT]** Upstream base router и 160 routed experts остаются immutable policy weights.

## Router program

- **[VERIFIED FACT]** Domains: Code Construction, Systems Architecture, Integrations, DevOps/SRE, Security/Compliance, QA/Review, Enterprise Communication, Governance/Escalation.
- **[ENGINEERING HYPOTHESIS]** Features: task type, requested tool, repository/state signals, risk class, permissions, policy hits, evidence gaps; secret/raw content исключается.
- **[ENGINEERING HYPOTHESIS]** Router emits Top-2 domain adapters + always-on shared Evidence/Policy adapter, scores, feature-schema hash и reason codes.
- **[RISK]** Collapse mitigation: balanced batches, entropy/load regularization, per-domain floor, route dropout и out-of-distribution fallback.

## World Model program

- **[VERIFIED FACT]** V0 = graph + append-only event ledger + policy engine; он остаётся state authority.
- **[ENGINEERING HYPOTHESIS]** V1 = 1.5–3B compact transition/risk model over canonical structured serialization; predicts delta, risk, reversibility, missing evidence и ask/plan/execute/escalate.
- **[VERIFIED FACT]** V1 никогда не пишет state напрямую: predictions сверяются с ledger/tool observations.
- **[RISK]** V1 не выпускается, если не превосходит V0 на held-out decisions; второй большой LLM не строится.

## Exact success metric и stop condition

- **[EXPERIMENT REQUIRED] Router gate:** Top-2 recall `>=90%`; no domain >35% routes; per-domain recall `>=80%`; audit record completeness `100%`.
- **[EXPERIMENT REQUIRED] V1 gate:** state-delta exact match `>=80%`; risk AUROC `>=0.90`; ECE `<=0.05`; decision accuracy `>=5 pp` выше V0; hallucinated authoritative state `0`.
- **[RISK] Stop:** collapse два evals, unversioned state input, ECE worsens дважды, leakage across tenants или V1 gain <5 pp.

## H200 Compute Plan

| Поле | Спецификация |
|---|---|
| Objective | **[EXPERIMENT REQUIRED]** Обучить router и отдельный compact transition model; это два tracked jobs. |
| Minimum H200 | **[ENGINEERING HYPOTHESIS]** 8× H200 SXM 141 GB, один Secure Cloud HGX Pod. |
| Recommended H200 | **[ENGINEERING HYPOTHESIS]** 32× H200 SXM 141 GB, 4 узла для parallel ablations. |
| Parallelism | **[ENGINEERING HYPOTHESIS]** Router/V1 min TP=1, PP=1, EP=1, CP=1, DP=8; rec V1 TP=2, DP=16; PP/EP/CP=1. |
| VRAM | **[ENGINEERING HYPOTHESIS]** H200 SXM 141 GB/GPU planning value; router/V1 не требуют 480B optimizer residency; full `M4` route eval планируется на отдельном 16/32-H200 inference allocation. |
| Network | **[VERIFIED FACT]** NVLink/NVSwitch intra-node. **[RISK]** Для recommended multi-node RunPod `ens*` допускается только с InfiniBand attestation; NCCL/IB parity и event-ledger replay обязательны. |
| Storage | **[ENGINEERING HYPOTHESIS]** 4 TB min / 10 TB rec Network Volume; encrypted registry хранит trace lineage/schema/router/V1. |
| Checkpoint | **[ENGINEERING HYPOTHESIS]** Каждые 1,000 steps/2 часа; independent router/V1 checkpoints with fresh optimizers; `M4` immutable. |
| Estimated wall-clock | **[ENGINEERING HYPOTHESIS]** Router 1–3 дня; V1 3–10 дней; ablations суммарно 7–18 дней. |
| Exact metric | **[EXPERIMENT REQUIRED]** Router 90% Top-2 recall/no >35%; V1 delta 80%, AUROC .90, ECE .05, +5 pp vs V0. |
| Stop/economic justification | **[RISK]** V1 run прекращается, если early scaling curve не способен дать +5 pp к V0; deterministic V0 — допустимый final artifact. |
| Artifact | **[VERIFIED FACT]** Router + routing audit; V1 checkpoint/calibration либо V1 no-go report. |

## Data controls

- **[VERIFIED FACT]** Trace содержит versioned `state_t`, `action_t`, observed `delta_t`, evidence и policy decision.
- **[RISK]** Missing observations не маркируются как negative outcomes; требуется explicit unknown mask.
- **[EXPERIMENT REQUIRED]** Split делать по repository/tenant/time, а не случайно по соседним events, чтобы исключить leakage.
- **[VERIFIED FACT]** Local control plane may orchestrate jobs and inspect anonymized metrics only; local auxiliary training/inference is forbidden.

