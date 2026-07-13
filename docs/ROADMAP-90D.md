# Independent E-01 — 90-дневная дорожная карта

## Terminal objective

- **[VERIFIED FACT]** Первые 90 дней заканчиваются evidence для code/schema/Hugging Face/Megatron parity, tokenizer candidate, governed corpus pipeline и 1B/7B proxy runs.
- **[VERIFIED FACT]** 90-дневный scope не включает 30B proxy, target-scale pretraining, posttraining release candidate или 480B run.
- **[ENGINEERING HYPOTHESIS]** `4–6T` accepted tokens — planning range target corpus, условный на scaling/economics evidence.
- **[EXPERIMENT REQUIRED]** Ни target architecture scale, ни token budget не получают approval до 30B proxy и отдельного investment gate.
- **[RISK]** Schedule pressure не является основанием пропустить rights, contamination, parity или recovery gates.

## Недели 1–2 — freeze contracts и schemas

- **[VERIFIED FACT]** Deliverables: architecture readiness schema, tokenizer rubric, PretrainCorpus/HYBRID-MIX/context contracts, split pretrain/posttrain eval plan, risk owners.
- **[EXPERIMENT REQUIRED]** CI валидирует schemas, deterministic parameter accounting и manifest completeness.
- **[RISK]** Несогласованные PyTorch/HF/Megatron semantics сделают proxy evidence непереносимым.
- **[VERIFIED FACT]** Exit: contracts versioned; неизвестные значения помечены `EXPERIMENT_REQUIRED`, а не заполнены claims.

## Недели 3–4 — data control plane

- **[VERIFIED FACT]** Deliverables: source registry, rights policy, PII/secrets quarantine, exact/near/semantic/AST dedup, contamination registry, tenant default-deny, lineage/Merkle builder.
- **[EXPERIMENT REQUIRED]** Проверить detectors на размеченных controls, воспроизводимость snapshot root и deletion impact drill.
- **[RISK]** Corpus volume без доказанных rights не является активом.
- **[VERIFIED FACT]** Exit: только signed approved snapshots читаются train identity; tenant namespaces недоступны.

## Недели 5–6 — tokenizer candidate

- **[ENGINEERING HYPOTHESIS]** Candidate обучается на governed representative sample independent corpus с code, multilingual, math и structured artifacts.
- **[EXPERIMENT REQUIRED]** Сравнить vocab/normalization candidates по fertility, bytes/token, fallback, round-trip, code whitespace, Unicode, identifiers, logs/schemas и embedding/head cost.
- **[RISK]** Tokenizer failure необратимо увеличит compute и ухудшит code/multilingual behavior target run.
- **[VERIFIED FACT]** Exit: один candidate и один fallback имеют immutable models, corpus hashes и regression report; final freeze ещё не объявлен.

## Недели 7–8 — executable architecture parity

- **[VERIFIED FACT]** Deliverables: minimal reference implementation, Hugging Face-compatible implementation, Megatron implementation/config, conversion and checkpoint schema.
- **[EXPERIMENT REQUIRED]** Проверить parameter counts, init statistics, forward logits, gradients, optimizer step, GQA/RoPE, hybrid attention masks, MoE routing, load balancing и checkpoint round trip на matched tiny configs.
- **[RISK]** Формальная config parity без numerical parity скрывает разные models.
- **[VERIFIED FACT]** Exit: frozen tolerance и signed parity report; failures остаются open blockers.

## Неделя 9 — H200 systems acceptance

- **[VERIFIED FACT]** Только H200 HGX/NVLink/NVSwitch и attested inter-node fabric разрешены для training evidence.
- **[EXPERIMENT REQUIRED]** NCCL, data streaming, optimizer sharding, expert/sequence parallelism, telemetry, distributed checkpoint and restore проверяются на reserved topology.
- **[RISK]** Низкий MFU или медленный checkpoint делает scaling plan экономически ложным.
- **[VERIFIED FACT]** Exit: measured throughput/MFU/checkpoint curves для proxy topology; это не target-scale result.

## Недели 10–11 — 1B proxy evidence

- **[EXPERIMENT REQUIRED]** 1B runs сравнивают architecture controls, tokenizer candidates, HYBRID-MIX candidates и context stages при matched compute.
- **[EXPERIMENT REQUIRED]** Reports: loss curves по strata, capability vector, context behavior, memorization, routing health, MFU, cost и restore.
- **[RISK]** 1B ranking может не сохраниться на MoE target scale.
- **[VERIFIED FACT]** Exit: invalid candidates eliminated по pre-registered gates; никакой target approval.

## Недели 12–13 — 7B proxy evidence и 90-day decision

- **[EXPERIMENT REQUIRED]** 7B confirmation проверяет выбранные architecture/tokenizer/mix/context hypotheses и перенос hyperparameters.
- **[EXPERIMENT REQUIRED]** Scaling fit включает uncertainty и план 30B discriminating experiments.
- **[RISK]** Один успешный seed или public benchmark не является evidence.
- **[VERIFIED FACT]** Exit bundle: code/schema/HF/Megatron parity, tokenizer candidate, governed corpus pipeline, immutable 1B/7B reports, 30B plan, budget/capacity request и explicit blockers.

## 90-day decision

- **[VERIFIED FACT]** `GO TO 30B PROXY` разрешает только 30B proxy, не target pretraining.
- **[VERIFIED FACT]** `CONDITIONAL GO` требует закрыть перечисленные parity/data/tokenizer/systems defects.
- **[VERIFIED FACT]** `NO-GO` обязателен при unresolved data rights, tenant boundary failure, contamination, unstable proxy convergence, checkpoint restore failure или неподтверждённой H200 topology.
- **[EXPERIMENT REQUIRED]** Approval target run рассматривается только после 30B evidence, capacity confirmation на 512/1024 H200 и полного budget-at-risk решения.
