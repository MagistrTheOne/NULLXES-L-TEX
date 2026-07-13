# Independent E-01 — promotion and release gates

## Rules

- **[VERIFIED FACT]** Gates conjunctive; failed hard gate means NO-GO for the next promotion.
- **[VERIFIED FACT]** `GO` applies only to the named stage. Proxy GO is not target-run or production GO.
- **[EXPERIMENT REQUIRED]** Thresholds are frozen before candidate comparison; no experiments are claimed here.

## G0 — architecture freeze

- **[EXPERIMENT REQUIRED]** Parameter accounting, initialization, forward/backward, GQA/RoPE, hybrid masks, MoE routing/load balance and checkpoint round-trip match across reference, Hugging Face and Megatron implementations within frozen tolerances.
- **[VERIFIED FACT]** PASS requires signed parity bundle and immutable code/config/schema hashes.
- **[RISK]** Config-only similarity is not parity.

## G1 — tokenizer freeze

- **[EXPERIMENT REQUIRED]** Candidate passes compression, byte fallback, normalization/round-trip, Unicode, code whitespace/identifiers, multilingual, logs/schema and 1B/7B capability ablations.
- **[VERIFIED FACT]** Vocabulary, special tokens and tokenizer training snapshot freeze before 30B proxy.
- **[RISK]** Tokenizer change after pretraining starts invalidates scaling comparison.

## G2 — corpus and HYBRID-MIX freeze

- **[VERIFIED FACT]** PASS requires signed PretrainCorpus snapshot, rights coverage, PII/secrets residual audit, dedup, contamination, tenant default-deny, deletion impact drill and reproducible Merkle root.
- **[EXPERIMENT REQUIRED]** Mix weights/caps/curriculum require proxy evidence.
- **[RISK]** `4–6T` is planning range until G4; volume alone cannot pass G2.

## G3 — 1B and 7B proxy gates

- **[EXPERIMENT REQUIRED]** At least two pre-registered seeds per promoted candidate, matched compute controls, stable convergence, capability vector, routing health, context tests, MFU and restore evidence.
- **[VERIFIED FACT]** PASS selects architecture/tokenizer/mix hypotheses for 30B; it does not authorize target pretraining.
- **[RISK]** Public benchmark gain cannot override held-out loss, contamination or instability.

## G4 — mandatory 30B proxy and target approval

- **[EXPERIMENT REQUIRED]** 30B proxy confirms scaling direction, hyperparameter transfer, MoE/router behavior, hybrid-attention economics, checkpoint recovery and capability.
- **[EXPERIMENT REQUIRED]** Scaling fit must include uncertainty for target loss/quality, tokens, wall clock and cost.
- **[VERIFIED FACT]** Target run remains blocked without signed 512/1024 H200 capacity, topology/NCCL/storage acceptance, budget-at-risk approval and stop conditions.
- **[RISK]** Failure of 30B confirmation returns to design; schedule and sunk cost grant no waiver.

## G5 — target pretrain convergence

- **[EXPERIMENT REQUIRED]** PASS requires stable loss/gradients, planned token accounting, routing health, no unresolved data incident, periodic capability checks, MFU above frozen floor and successful recovery drills.
- **[VERIFIED FACT]** Stop conditions include sustained divergence, router collapse, data-rights incident, contamination, checkpoint loss or breached budget.
- **[RISK]** Completing token budget is not convergence evidence.

## G6 — context curriculum stages

- **[EXPERIMENT REQUIRED]** Each stage independently passes short-context retention, length-stratified loss, retrieval/multi-hop code, throughput/MFU and restore.
- **[VERIFIED FACT]** Failed stage does not invalidate the last passing shorter-context checkpoint, but blocks longer-context claim.
- **[RISK]** 128K–256K remains deferred until kernel and quality evidence.

## G7 — posttrain Enterprise Action

- **[EXPERIMENT REQUIRED]** SFT, preference and executable RL stages separately pass four LÆTEX-Bench action tracks, capability retention, tool validity, governance and NATIVE-IDENTITY.
- **[VERIFIED FACT]** Persona leakage hard gate is `0/10 000`; any critical unauthorized side effect fails promotion.
- **[VERIFIED FACT]** External deny-by-default policy enforcement is mandatory; model refusal alone is insufficient.

## G8 — BF16 master

- **[VERIFIED FACT]** BF16 master is immutable, content-addressed and linked to architecture/tokenizer/corpus/pretrain/posttrain manifests.
- **[EXPERIMENT REQUIRED]** Two clean runs reproduce pretrain capability, four-track VETCR, identity, governance, rollback, latency and cost within frozen tolerance.
- **[RISK]** Missing hash, evidence or reproducibility means no master promotion.

## G9 — FP8 parity

- **[VERIFIED FACT]** FP8 is a serving derivative, never the source BF16 master.
- **[EXPERIMENT REQUIRED]** PASS requires numerical/load stability, pretrain capability non-inferiority, four-track VETCR, `0/10 000` identity, governance parity and measured throughput/cost gain.
- **[RISK]** Microbenchmark speedup cannot override end-to-end quality.

## Final decision

- **[VERIFIED FACT]** Production GO requires G0–G9 and signed evidence bundles.
- **[VERIFIED FACT]** CONDITIONAL GO allows only bounded R&D without production data, credentials or writes.
- **[EXPERIMENT REQUIRED]** Current status: `UNVERIFIED / TARGET RUN NOT APPROVED / NOT RELEASED`.
