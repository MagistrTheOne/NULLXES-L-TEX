# FOUNDATION PLANE

## Назначение

- **VERIFIED FACT:** Foundation Plane фиксирует E-01 backbone `Qwen/Qwen3-Coder-Next-Base` и происхождение derivative model.
- **VERIFIED FACT:** Model card: 80B total/3B activated, 48 layers, hidden 2048, hybrid Gated DeltaNet/Gated Attention, 512 experts, Top-10 + shared, native 262 144 context.
- **RISK:** Model card не является доказательством качества LÆTEX на enterprise tasks.

## Inputs / outputs

- **ENGINEERING HYPOTHESIS:** Inputs: tokenizer-preserving token streams, versioned training manifests, LÆTEX role/tool contracts, adapter selection и bounded CodeWorld context.
- **ENGINEERING HYPOTHESIS:** Outputs: token probabilities или schema-constrained action proposals; outputs не являются permissions, evidence или authoritative state.

## Trust boundary

- **VERIFIED FACT:** Checkpoint и model server находятся внутри isolated H200 compute boundary; prompts входят только после tenant authorization и policy projection.
- **VERIFIED FACT:** Foundation не получает raw credentials, secret values или unrestricted tenant corpus.
- **RISK:** Prompt injection и memorized upstream behavior остаются возможными; runtime обязан считать output недоверенным.

## Authoritative state

- **VERIFIED FACT:** Model weights авторитетны только для versioned behavior artifact. CodeWorld/event ledger/tool observations авторитетны для operational state.
- **VERIFIED FACT:** Model-generated claims без evidence ID не обновляют state.

## Tenant boundary

- **VERIFIED FACT:** Base weights общие; tenant data, KV/prefix cache, adapters, logs и context snapshots namespace/encryption-isolated.
- **RISK:** Shared batching/cache может создать side channel; cross-tenant cache запрещён до отдельного security proof.

## Adaptation policy

- **ENGINEERING HYPOTHESIS:** E-01 начинает с LoRA/adapters на attention/output projections и selected dense/shared paths; embeddings, tokenizer и internal MoE router заморожены.
- **EXPERIMENT REQUIRED:** Selective unfreezing layer norms/shared experts/router допускается только по ablation с regression suite.
- **RISK:** Internal router adaptation может вызвать expert collapse и catastrophic forgetting; full-parameter tuning требует отдельного compute/quality gate.
- **ENGINEERING HYPOTHESIS:** Replay mixture исходного coding data, low learning rate, gradient monitoring и frozen baseline eval ограничат forgetting.

## Failure modes

- **RISK:** Hallucinated state, invalid tool syntax, identity leakage, context truncation, catastrophic forgetting, router drift и OOM на long context.
- **EXPERIMENT REQUIRED:** Каждая failure class имеет frozen regression set и severity-specific release threshold.

## Observability

- **ENGINEERING HYPOTHESIS:** Логируются model/checkpoint hash, adapter versions, tokenizer hash, context token counts, cache policy, route, latency, finish reason и schema validation; content redacted по policy.
- **VERIFIED FACT:** Training lineage связывает source manifest, code/container digest, H200 topology, seeds, optimizer state и checkpoint.

## Release artifact

- **VERIFIED FACT:** Signed checkpoint reference, tokenizer/chat template, adapter compatibility manifest, internal model card, upstream notices, eval dossier и reproducibility record.
