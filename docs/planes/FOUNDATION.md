# FOUNDATION PLANE

## Decision

- **VERIFIED FACT:** ADR-0007 принимает independent from-scratch E-01 без external weight parent, checkpoint initialization или inherited tokenizer.
- **ENGINEERING HYPOTHESIS:** Target architecture: 64 layers; `d_model=8192`; GQA `64Q/8KV`; head dimension 128; hybrid attention `7 local : 1 global`; local window 16 384; 144 routed experts + 1 shared expert; Top-6; expert `d_ff=2048`; vocabulary 128K; context target 262 144; BF16 master.
- **EXPERIMENT REQUIRED:** `~478.9B total / ~34.4B active` — provisional estimates pending executable parameter-count proxy and exact MoE placement, shared-expert, embedding/output and attention accounting.
- **VERIFIED FACT:** Qwen не является weight parent, tokenizer source или runtime dependency; допустимые benchmark/teacher roles ограничены ADR-0009.

## Model boundary

- **ENGINEERING HYPOTHESIS:** Inputs: token streams custom tokenizer T0, versioned context slices, role/tool contracts and policy projections.
- **ENGINEERING HYPOTHESIS:** Outputs: token probabilities and schema-constrained action proposals; outputs are not permissions, evidence or authoritative state.
- **VERIFIED FACT:** Operational truth remains in CodeWorld, event ledger and tool observations.
- **RISK:** Prompt injection, hallucinated state and unsafe actions remain possible even after successful pretraining/post-training; runtime treats model output as untrusted.

## Architecture validation

- **EXPERIMENT REQUIRED:** Proxy suite must validate parameter count, forward/backward numerical stability, router entropy, expert utilization, capacity overflow, load balance, checkpoint resume and scale-transfer assumptions.
- **EXPERIMENT REQUIRED:** Hybrid attention must be trained as part of scratch pretraining and tested at each context curriculum stage; a 262 144 target is not a verified capability before long-context evaluation.
- **ENGINEERING HYPOTHESIS:** FP32 router logits/critical reductions, BF16 master weights and fused H200 kernels are starting implementation choices, not verified production settings.
- **RISK:** Top-6 across 144 experts raises all-to-all traffic; H200 EP/TP/PP/CP mapping and provider-attested InfiniBand must pass representative communication tests.
- **RISK:** Shared expert cost, 128K embeddings and global-attention layers can move active/total estimates materially.

## Scratch lineage

- **VERIFIED FACT:** Canonical chain is `C0 → T0 → R0 → P0..Pn → G0 → PT0..PTn → B0 → SFT0 → PREF0 → RL0 → M0`.
- **VERIFIED FACT:** `R0` is reproducible random initialization; no external model hash appears in the weight-parent graph.
- **VERIFIED FACT:** `B0` and `M0` are immutable BF16 artifacts; any FP8 or other serving export is a parity-gated derivative and never a training parent.
- **VERIFIED FACT:** Teacher candidates can be data parents only through ADR-0009 manifests; teacher weights cannot be weight parents.
- **RISK:** Full-scale pretraining before signed `G0` is prohibited.

## Compute and locality

- **VERIFIED FACT:** Training, evaluation, checkpoint conversion, teacher generation and model inference are H200-only.
- **VERIFIED FACT:** Production topology requires homogeneous NVIDIA H200 HGX nodes, NVLink/NVSwitch intra-node and provider-attested InfiniBand inter-node.
- **VERIFIED FACT:** Local control plane may develop code/configs, orchestrate jobs and inspect redacted metrics; it stores no weights, optimizer states, training corpus or customer payloads.
- **EXPERIMENT REQUIRED:** Before paid scale-up: NCCL acceptance, storage throughput, atomic checkpoint publish, resume/recovery and budget cap must pass.

## Release artifact

- **VERIFIED FACT:** Release dossier contains C0/T0/R0 provenance, proxy evidence, signed G0, full checkpoint lineage, BF16 M0, parity-approved serving derivative, eval artifacts, SBOM, model card and rollback pointer.
- **RISK:** Documentation, parameter arithmetic or a successful load test alone does not prove model quality or economic viability.
