# ADR-0010: Scratch pretrain/post-train lineage

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Дата: 2026-07-13.
- **VERIFIED FACT:** Область: end-to-end E-01 model lineage.

## Канонический lineage

1. **VERIFIED FACT:** `C0` — approved corpus manifests, source/license/PII decisions, dedup and contamination records.
2. **VERIFIED FACT:** `T0` — frozen custom tokenizer, vocabulary, normalization and special-token contract.
3. **VERIFIED FACT:** `R0` — reproducible random initialization recipe without external checkpoint parent.
4. **ENGINEERING HYPOTHESIS:** `P0..Pn` — H200 proxy runs for architecture, optimizer, MoE routing, attention and scale-transfer validation.
5. **EXPERIMENT REQUIRED:** `G0` — signed architecture/data/systems/budget gate approving full scale.
6. **ENGINEERING HYPOTHESIS:** `PT0..PTn` — resumable full E-01 pretraining checkpoints; accepted terminal artifact is immutable BF16 `B0`.
7. **ENGINEERING HYPOTHESIS:** `SFT0 → PREF0 → RL0` — separately versioned post-training stages with frozen evaluations and rollback parents.
8. **VERIFIED FACT:** `M0` — BF16 master candidate only after release gates; lower-precision serving artifacts are derivatives and never lineage parents.

## Controls

- **VERIFIED FACT:** Каждый artifact хранит parent IDs, code/container digest, config, seeds, dataset/tokenizer hashes, H200 topology, optimizer state policy, metrics and operator identity.
- **VERIFIED FACT:** Checkpoints и optimizer states находятся в isolated remote object storage/registry; локальная выгрузка weights запрещена.
- **EXPERIMENT REQUIRED:** Resume, corruption detection, atomic publish and disaster recovery проверяются до full-scale run.
- **RISK:** Teacher datasets могут быть data parents с ADR-0009 provenance, но teacher weights никогда не являются weight parents.
- **RISK:** FP8/другой serving format не может быть parent BF16 pretraining или post-training artifact.
- **RISK:** Promotion без raw eval artifacts, lineage completeness и rollback pointer запрещён.
