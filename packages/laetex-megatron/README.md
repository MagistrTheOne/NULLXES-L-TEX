# laetex-megatron

Pure compatibility contracts for translating a LÆTEX target shape into
Megatron-Core arguments, validating parallel topology, planning checkpoint key
conversion, and describing custom ModuleSpecs.

Megatron-Core and Transformer Engine are optional and are not imported by the
pure contract APIs. Without both dependencies, `STUB_MODE` is true. Only
`materialize_module_spec()` requires the runtime and raises a clear import error
otherwise.

```text
pip install "laetex-megatron[megatron]"
```

Install the runtime extra only in the pinned, approved H200 container. This
package neither initializes `torch.distributed` nor probes CUDA.

## Important boundaries

- `TargetModelConfig` defaults describe E-01. Sigmoid routing, shared experts,
  and hybrid attention are future target options, not claims about E-01.
- `to_megatron_args()` produces a version-neutral argument record. An audited
  launcher must adapt it to the exact pinned Megatron-Core API.
- Topology uses `world_size = TP * PP * CP * DP`; EP partitions DP and must
  divide DP. It is not multiplied into world size a second time.
- Weight mapping emits a deterministic tensor transformation plan. It does not
  concatenate, transpose, shard, allocate, or write tensors.
- ModuleSpec placeholders define interfaces only. A custom audited
  implementation class is required before materialization.

See `PARITY.md` before any H200 conversion or runtime job.
