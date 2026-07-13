# Источники, evidence classes и pinning

> **VERIFIED FACT —** Проверено: 2026-07-13.
> **VERIFIED FACT —** Scope: independent E-01 design, external benchmark/teacher references and H200 infrastructure.
> **VERIFIED FACT —** Architecture targets are project decisions, not external verified model facts.

## Canonical internal decisions

- **VERIFIED FACT:** [`adr/0007-independent-from-scratch-e01.md`](adr/0007-independent-from-scratch-e01.md) accepts independent E-01 and supersedes ADR-0006.
- **VERIFIED FACT:** [`adr/0008-custom-tokenizer.md`](adr/0008-custom-tokenizer.md) accepts the custom tokenizer and supersedes ADR-0001.
- **VERIFIED FACT:** [`adr/0009-qwen-reference-teacher-firewall.md`](adr/0009-qwen-reference-teacher-firewall.md) limits Qwen to benchmark and optional offline synthetic teacher.
- **VERIFIED FACT:** [`adr/0010-scratch-pretrain-post-train-lineage.md`](adr/0010-scratch-pretrain-post-train-lineage.md) defines the scratch lineage.
- **EXPERIMENT REQUIRED:** Target parameter counts and systems feasibility require generated artifacts; documentation consensus is not validation.

## E-01 target facts

- **ENGINEERING HYPOTHESIS:** 64 layers, `d_model=8192`, GQA `64Q/8KV`, head dimension 128.
- **ENGINEERING HYPOTHESIS:** Hybrid pattern 7 local + 1 global, local window 16 384.
- **ENGINEERING HYPOTHESIS:** 144 routed experts + 1 shared expert, Top-6, expert `d_ff=2048`.
- **ENGINEERING HYPOTHESIS:** Vocabulary target 128K, context target 262 144, BF16 master.
- **EXPERIMENT REQUIRED:** `~478.9B total / ~34.4B active` must be validated by executable parameter-count proxy and frozen accounting rules.

## Qwen reference boundary

- **VERIFIED FACT:** Qwen is not a weight parent, tokenizer source, initialization source or runtime dependency E-01.
- **VERIFIED FACT:** Historical derivative decisions are archived under [`branches/HISTORICAL/qwen-derivative-e01/`](branches/HISTORICAL/qwen-derivative-e01/).
- **VERIFIED FACT:** Reference model URL: <https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct>.
- **VERIFIED FACT:** Alternative reference URL: <https://huggingface.co/Qwen/Qwen3-Coder-Next-Base>.
- **RISK:** Mutable model cards, revisions, licenses and benchmark claims cannot be copied into an experiment manifest without exact pinning and legal review.
- **EXPERIMENT REQUIRED:** Any teacher run must pin exact revision/files/license, hash retrieved artifacts, record prompts/config and remain H200-only under ADR-0009.
- **RISK:** Upstream benchmark numbers are not LÆTEX results and cannot establish E-01 quality.

## NVIDIA H200

- **VERIFIED FACT:** Official product page: <https://www.nvidia.com/en-us/data-center/h200/>.
- **VERIFIED FACT:** The NVIDIA page lists H200 SXM with 141 GB HBM3e, 4.8 TB/s memory bandwidth and 900 GB/s NVLink.
- **RISK:** Product specifications do not establish E-01 memory fit, MFU, throughput or wall-clock.

## RunPod infrastructure references

- **VERIFIED FACT:** GPU types: <https://docs.runpod.io/references/gpu-types>.
- **VERIFIED FACT:** Instant Clusters: <https://docs.runpod.io/instant-clusters>.
- **VERIFIED FACT:** Cluster configuration/NCCL: <https://docs.runpod.io/instant-clusters/configuration>.
- **VERIFIED FACT:** Network Volumes: <https://docs.runpod.io/storage/network-volumes>.
- **RISK:** Provider pages do not prove current quota, price, exact topology, InfiniBand semantics, sustained NCCL bandwidth or storage SLA for a specific allocation.
- **EXPERIMENT REQUIRED:** Every allocation requires written fabric/topology attestation and measured NCCL/storage/recovery acceptance before model workloads.

## Source and run policy

- **VERIFIED FACT:** Canonical model lineage begins with dataset/tokenizer artifacts and R0 random initialization; no external model revision appears in the weight-parent graph.
- **ENGINEERING HYPOTHESIS:** Registry records URLs, retrieval timestamps, hashes, license/consent state, transformations, code/container digest, H200 topology and operator identity.
- **EXPERIMENT REQUIRED:** Before architecture freeze, parameter-count source code and generated report become signed references in addition to prose.
- **RISK:** No quality, latency, token budget, H200 count or cost claim is verified until backed by a reproducible run artifact.
