# FOUNDATION PLANE

## Назначение

- **VERIFIED FACT:** Foundation Plane фиксирует прямой E-01 backbone `Qwen/Qwen3-Coder-480B-A35B-Instruct` и происхождение derivative model.
- **VERIFIED FACT:** Official card/config: causal LM, `Pretraining & Post-training`, 480B total/35B activated, 62 layers, hidden 6144, GQA 96Q/8KV, head dimension 128, 160 routed experts, Top-8, no shared expert (`shared_expert_intermediate_size=0`), expert intermediate 2560, vocabulary 151 936, native context 262 144, BF16, Apache-2.0.
- **VERIFIED FACT:** Отдельно выпущенный официальный 480B Base checkpoint в проверенных источниках не идентифицирован; upstream E-01 является Instruct.
- **VERIFIED FACT:** Official Hugging Face API evidence, проверенный 2026-07-13, закрепляет revision `9d90cf8fca1bf7b7acca42d3fc9ae694a2194069`, safetensors BF16 parameter count `480154875392`, `usedStorage=960313541352`, наличие `LICENSE` в file list и metadata `apache-2.0`.
- **RISK:** Commit SHA является revision identifier, а не SHA-256 hash весов. Training заблокирован до RunPod source preflight всех 241 shards, config, tokenizer, chat template и license/notices.
- **VERIFIED FACT:** 80B/3B Next Base не является E-01 foundation и может существовать только как исторически отвергнутая/альтернативная branch.
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

- **ENGINEERING HYPOTHESIS:** Канонический lineage: `S0 → A1 → M1 → A2 → M2 → A3 → M3 → A4 → M4 → FP8`; `A1..A4` — retained adapters, `M1..M4` — immutable BF16 merges, FP8 — только serving derivative после parity.
- **ENGINEERING HYPOTHESIS:** Embeddings, tokenizer, internal MoE router и все routed experts на начальных стадиях заморожены. LoRA targets выбираются только после module inventory и memory profiling exact pinned checkpoint.
- **ENGINEERING HYPOTHESIS:** Broad CPT исключён из default recipe: upstream уже post-trained, и language-model objective может разрушить instruction/tool alignment.
- **EXPERIMENT REQUIRED:** Узкий CPT, layer unfreezing, router adaptation или expert adaptation допускаются только как отдельные ablations после доказанного adapter ceiling и с frozen regression suite.
- **EXPERIMENT REQUIRED:** M1, M2, M3 и M4 обязаны пройти merge integrity, weight-delta audit, identity/tool/coding/governance evaluation и reproducibility check; M4 дополнительно проходит release suite.
- **EXPERIMENT REQUIRED:** FP8 serving derivative получает release status только после parity с BF16 M4 по VETCR, critical failures, tool schema validity и bounded numerical drift.
- **RISK:** Router/expert adaptation может вызвать routing collapse, expert drift и catastrophic forgetting; full-parameter tuning требует отдельного compute/economic gate.
- **RISK:** Даже LoRA merge может необратимо испортить BF16 master при ошибке dtype, scaling или target mapping; S0/M1/M2/M3/M4 хранятся как отдельные immutable artifacts.

## Failure modes

- **RISK:** Hallucinated state, invalid tool syntax, identity leakage, upstream persona persistence, alignment loss, context truncation, catastrophic forgetting, router drift и OOM на long context.
- **EXPERIMENT REQUIRED:** Каждая failure class имеет frozen regression set и severity-specific release threshold.

## Observability

- **ENGINEERING HYPOTHESIS:** Логируются model/checkpoint hash, adapter versions, tokenizer hash, context token counts, cache policy, route, latency, finish reason и schema validation; content redacted по policy.
- **VERIFIED FACT:** Training lineage связывает source manifest, code/container digest, H200 topology, seeds, optimizer state и checkpoint.

## Release artifact

- **VERIFIED FACT:** Release artifact содержит signed BF16 M4 reference, FP8 derivative reference после parity, tokenizer/chat template, полный `S0 → A1 → M1 → A2 → M2 → A3 → M3 → A4 → M4 → FP8` lineage, adapter compatibility manifest, internal model card, pinned upstream revision, upstream notices, eval dossier и reproducibility record.
