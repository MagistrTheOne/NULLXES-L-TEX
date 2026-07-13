# Independent E-01 — speed / cost / quality strategy

## Status

- **[VERIFIED FACT]** E-01 has no inherited checkpoint or verified benchmark result.
- **[ENGINEERING HYPOTHESIS]** `4–6T` accepted pretraining tokens is a planning range conditional on proxy scaling and economics.
- **[EXPERIMENT REQUIRED]** Architecture scale, active parameters, context envelope, training wall clock and serving latency remain unverified until staged proxy evidence.
- **[RISK]** Tokens/s, MFU or benchmark score alone cannot establish cost per useful capability or verified enterprise task.

## Training economics

- **[VERIFIED FACT]** Target training approval follows 1B → 7B → mandatory 30B proxies.
- **[EXPERIMENT REQUIRED]** Every stage reports useful tokens/s, model FLOPs utilization, data wait, collective time, router dispatch, pipeline bubbles, checkpoint overhead, failures/restarts and cost.
- **[VERIFIED FACT]** Target capacity options are assessed at `512` and `1024` NVIDIA H200; neither allocation is assumed available.
- **[RISK]** Low MFU, weak scaling efficiency or slow checkpoint recovery can make technically valid architecture economically invalid.
- **[EXPERIMENT REQUIRED]** Target approval requires uncertainty-bounded cost for 4T, 5T and 6T scenarios and explicit stop-loss checkpoints.

## Architecture and context trade-offs

- **[ENGINEERING HYPOTHESIS]** MoE lowers active compute relative to total capacity, but EP communication and router imbalance may erase savings.
- **[ENGINEERING HYPOTHESIS]** Hybrid local/global attention can reduce long-context FLOPs, but only if kernels sustain H200 efficiency without distant-dependency regression.
- **[EXPERIMENT REQUIRED]** Full-attention controls compare quality, HBM, throughput and MFU at each context stage.
- **[RISK]** Advertising 256K from config without native context-stage evidence is prohibited.

## Pretrain quality

- **[EXPERIMENT REQUIRED]** Quality is a vector: held-out loss, code execution, math, language/multilingual, knowledge calibration, context, memorization and MoE routing health.
- **[VERIFIED FACT]** A single aggregate benchmark cannot promote tokenizer, mix, architecture or checkpoint.
- **[RISK]** Improving public evals while held-out loss or contamination worsens is not a gain.

## Posttrain action efficiency

- **[VERIFIED FACT]** Posttrain evaluation remains split into four LÆTEX-Bench tracks and uses VETCR as action KPI.
- **[ENGINEERING HYPOTHESIS]** Structured state, prefix/repository caching, constrained tools, continuous batching and parallel read-only verification can reduce time-to-verified-completion.
- **[VERIFIED FACT]** Cache keys are tenant, repository-state, policy, permission, tokenizer/template and runtime scoped; cross-tenant reuse is forbidden.
- **[EXPERIMENT REQUIRED]** Serving engine and BF16/FP8 bakeoffs use identical checkpoints, workload, tool budgets and verification.
- **[RISK]** Lower cost/token can increase cost per verified task through retries, invalid actions or weaker verification.

## Latency targets

- **[ENGINEERING HYPOTHESIS]** Warm interactive TTFT, architecture-plan, small-patch and PR-level targets are frozen only after target architecture and serving topology exist.
- **[EXPERIMENT REQUIRED]** Reports separate queue, prefill, decode, tool, sandbox, verifier, retry and human-approval time; p50/p95 and cold/warm/cache strata are mandatory.
- **[RISK]** Carrying latency numbers from an unrelated 480B checkpoint into scratch E-01 would be false precision.

## FP8

- **[VERIFIED FACT]** BF16 remains canonical master; FP8 is a serving derivative.
- **[EXPERIMENT REQUIRED]** FP8 promotion requires pretrain capability, four-track VETCR, native identity, governance, numerical stability and end-to-end cost/latency parity evidence.
- **[RISK]** Kernel-level speedup without full workload parity is insufficient.
