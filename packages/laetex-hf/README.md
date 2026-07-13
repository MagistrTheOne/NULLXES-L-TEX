# laetex-hf

Compatibility layer between the Transformers lifecycle and the authoritative
`laetex-core` implementation. This package does not contain model kernels or
weights and does not permit local model execution.

## Install

```text
pip install "laetex-hf[transformers]"
```

Importing `laetex_hf` without Transformers is supported. Accessing
`LaetexConfig`, `LaetexForCausalLM`, or registration APIs then raises an
actionable `MissingTransformersError`.

## Contract

- `LaetexConfig.model_type` is `laetex_moe`.
- `LaetexConfig.save_pretrained()` / `from_pretrained()` provide the standard
  tiny config-directory round trip.
- `LaetexForCausalLM` owns a `core_model` module and delegates forward,
  embedding, generation-input, and cache-reorder operations.
- Standard `save_pretrained()` / `from_pretrained()` use keys below the
  deterministic `core_model.` prefix. Construction requires a compatible
  installed `laetex-core`; no fallback neural network is supplied.
- `register_with_transformers()` explicitly installs AutoConfig and
  AutoModelForCausalLM registrations. Importing the package does not mutate
  global Auto mappings.

## Minimal config round trip

```python
from laetex_hf import LaetexConfig, register_with_transformers

register_with_transformers()
config = LaetexConfig(hidden_size=64, num_attention_heads=4, num_key_value_heads=2, head_dim=16)
config.save_pretrained("/tmp/laetex-config")
restored = LaetexConfig.from_pretrained("/tmp/laetex-config")
```

The tiny values above test serialization only. They are not an approved LÆTEX
training or inference profile.

See `PARITY.md` before claiming checkpoint compatibility.
