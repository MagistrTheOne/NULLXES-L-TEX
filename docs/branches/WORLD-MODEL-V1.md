# WORLD-MODEL-V1 — learned transition model research branch

## Preconditions

- **VERIFIED FACT:** V1 не начинается до эксплуатации V0 graph + event ledger + policy engine на replayable research traces.
- **EXPERIMENT REQUIRED:** Dataset должен содержать versioned tuples `(state_t, action_t, observed_delta_t)` с provenance, policy decision, missingness mask и outcome confidence.
- **RISK:** Наблюдения runtime не равны causal ground truth; selection bias и unobserved side effects могут сделать transition model уверенно неверной.

## Scope

- **ENGINEERING HYPOTHESIS:** Compact 1.5–3B transition model предсказывает typed delta, risk events, reversibility class, missing evidence и disposition `ask|plan|execute|escalate`.
- **VERIFIED FACT:** V1 не пишет authoritative state и не обходит policy engine; его outputs — advisory predictions с calibrated uncertainty.
- **VERIFIED FACT:** Второй большой general LLM не нужен: задача ограничена structured transition prediction, а latency и auditability важнее свободной генерации.

## Architecture hypothesis

- **ENGINEERING HYPOTHESIS:** Decoder-only transformer с structured serialization, constrained decoding и multi-head classification/regression heads — baseline; graph encoder добавляется только при доказанном выигрыше.
- **ENGINEERING HYPOTHESIS:** Inputs включают bounded state projection, action schema, policy references и evidence summary; tenant identifiers pseudonymized, secret values исключены.
- **ENGINEERING HYPOTHESIS:** Outputs валидируются JSON Schema и связываются с asset/version IDs; natural-language rationale не используется как decision authority.

## Training objectives

- **ENGINEERING HYPOTHESIS:** Loss = delta token loss + affected-asset classification + calibrated risk loss + reversibility ordinal loss + evidence-missingness loss + disposition loss.
- **EXPERIMENT REQUIRED:** Сравнить learned model с deterministic rules, gradient-boosted structured baseline и retrieval-only nearest trace.
- **EXPERIMENT REQUIRED:** Оценивать temporal holdout, unseen repository holdout и tenant-disjoint opt-in holdout.

## Compute and data governance

- **VERIFIED FACT:** Training/inference research с weights выполняется только на RunPod H200; no local model compute.
- **VERIFIED FACT:** Raw tenant traces не входят в общий training corpus без explicit, revocable, scoped opt-in и separate lineage.
- **RISK:** Даже обезличенные action graphs могут раскрывать enterprise topology; требуется privacy review и membership-inference testing.

## Stop gates

- **EXPERIMENT REQUIRED:** V1 должен снижать missed-risk rate и missing-evidence rate против V0 baseline при заданном false-escalation budget.
- **EXPERIMENT REQUIRED:** Calibration error, abstention quality и out-of-distribution detection проходят frozen gates.
- **RISK:** Любое ухудшение critical-risk recall, cross-tenant leakage или зависимость runtime availability от V1 блокирует интеграцию.

## Release artifact

- **VERIFIED FACT:** Research checkpoint reference, tokenizer/serialization contract, feature manifest, calibration map, model card, dataset lineage, eval dossier и shadow-mode integration spec.
