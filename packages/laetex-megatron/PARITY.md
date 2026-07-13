# Megatron parity checklist

- [ ] Pin Megatron-Core, Transformer Engine, CUDA, NCCL, and container digests.
- [ ] Confirm every emitted argument against the pinned Megatron API.
- [ ] Inventory the immutable source checkpoint and map every key exactly once.
- [ ] Specify Q/K/V concatenation order and GQA row layout with golden tensors.
- [ ] Specify SwiGLU gate/up concatenation order with golden tensors.
- [ ] Prove TP and EP shard offsets for all experts, including uneven failure cases.
- [ ] Reject unknown, duplicate, missing, or shape-incompatible checkpoint keys.
- [ ] Compare unsharded core and Megatron logits in BF16 within an approved tolerance.
- [ ] Compare gradients and optimizer-step deltas on a tiny synthetic shape.
- [ ] Validate PP ownership, tied/untied embeddings, and final norm placement.
- [ ] Validate context-parallel sequence partitioning and cache layout.
- [ ] Implement and test custom hybrid attention, sigmoid router, and shared expert specs.
- [ ] Run NCCL/fabric preflight and checkpoint-resume tests on the approved H200 cluster.
- [ ] Record topology, seeds, package versions, mapping-contract version, and artifact hashes.

No H200, distributed, CUDA, conversion, or parity run has been performed here.
