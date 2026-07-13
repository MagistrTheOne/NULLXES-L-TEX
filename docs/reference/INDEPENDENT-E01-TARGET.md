# Independent E-01 target reference

- **VERIFIED FACT:** Authority: ADR-0007, ADR-0008, ADR-0009 and ADR-0010.
- **VERIFIED FACT:** This reference is a human-readable target, not an executable config or validated parameter report.

## Frozen decision inputs

| Field | Value |
|---|---|
| Layers | **ENGINEERING HYPOTHESIS:** 64 |
| Model width | **ENGINEERING HYPOTHESIS:** 8192 |
| Attention | **ENGINEERING HYPOTHESIS:** 64 Q heads / 8 KV heads / head dimension 128 |
| Pattern | **ENGINEERING HYPOTHESIS:** 7 local layers + 1 global layer |
| Local window | **ENGINEERING HYPOTHESIS:** 16 384 |
| MoE | **ENGINEERING HYPOTHESIS:** 144 routed experts + 1 shared expert |
| Routing | **ENGINEERING HYPOTHESIS:** Top-6 |
| Expert width | **ENGINEERING HYPOTHESIS:** `d_ff=2048` |
| Vocabulary | **ENGINEERING HYPOTHESIS:** 128K |
| Context | **ENGINEERING HYPOTHESIS:** target 262 144 |
| Master precision | **VERIFIED FACT:** BF16 |
| Scale estimate | **EXPERIMENT REQUIRED:** `~478.9B total / ~34.4B active` |

## Validation contract

- **EXPERIMENT REQUIRED:** Executable model builder must emit total parameters, trainable parameters, active parameters per token and per-component breakdown.
- **EXPERIMENT REQUIRED:** Report must state embeddings/output tying, MoE layer placement, shared-expert activation, router accounting, biases/norms and local/global attention projection equality.
- **EXPERIMENT REQUIRED:** Forward/backward proxy must match generated count and demonstrate stable routing before architecture freeze.
- **RISK:** The stated estimates can change materially if every layer is not MoE, shared expert semantics differ, embeddings are untied or implementation adds dense FFN blocks.
- **RISK:** Active parameter count is execution-policy dependent and must not be inferred from total count alone.
