# Hugging Face parity checklist

- [ ] Pin a mutually compatible `laetex-core`, Transformers, and PyTorch build.
- [ ] Round-trip every core config field without silent default substitution.
- [ ] Verify `AutoConfig` and `AutoModelForCausalLM` from a saved tiny artifact.
- [ ] Compare wrapper and direct-core logits for identical seeds and inputs.
- [ ] Compare loss, cache shapes, generation tokens, and cache reordering.
- [ ] Save, reload, and byte-audit all state-dict keys under `core_model.`.
- [ ] Reject missing, unexpected, duplicated, or shape-changed parameters.
- [ ] Verify BF16 checkpoint shard indexes without loading on the local control plane.
- [ ] Exercise 32K, 64K, and native-window behavior on the approved H200 inference cluster.
- [ ] Record numerical tolerances, package versions, checkpoint digest, and H200 topology.

No item in this checklist is currently a verified benchmark result.
