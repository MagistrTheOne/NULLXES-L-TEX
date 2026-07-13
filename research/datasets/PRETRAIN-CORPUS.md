# PretrainCorpus contract

## Назначение и масштаб

- **[VERIFIED FACT]** PretrainCorpus — governed набор для независимого pretraining E-01 с нуля; он не является CPT, distillation corpus или производной от checkpoint третьей стороны.
- **[ENGINEERING HYPOTHESIS]** Плановый target `4–6T` accepted tokens достаточен как диапазон для budget modelling, но не является утверждённым token budget.
- **[EXPERIMENT REQUIRED]** Финальный token budget утверждается только после scaling-law evidence на 1B/7B/30B proxies, оценки irreducible loss по доменам, throughput/MFU и полной экономики H200 target run.
- **[RISK]** Раннее объявление `4–6T` обязательством создаст sunk-cost pressure и может зафиксировать неэффективный data mix.

## Классы данных

- **[ENGINEERING HYPOTHESIS]** Candidate mix включает natural language, code, math/STEM, structured enterprise artifacts, multilingual text и verified synthetic data.
- **[VERIFIED FACT]** Точный mix задаётся только versioned `HYBRID-MIX` manifest; проценты без proxy ablation не считаются результатом.
- **[VERIFIED FACT]** Post-training наборы CodeWorld, SystemWorld, Enterprise Voice, ActionWorld и GovernanceSet логически и физически отделены от pretrain snapshots.
- **[RISK]** Смешивание action labels, hidden eval или шаблонов identity в broad pretrain затрудняет attribution и повышает contamination.

## Admission pipeline

**[VERIFIED FACT]** Обязательный pipeline:

`source registration → quarantine → rights decision → PII/secrets scan → normalization → language/domain classification → quality scoring → exact/near/semantic/structural dedup → eval contamination scan → mixture eligibility → immutable shard → signed snapshot`

- **[VERIFIED FACT]** Default deny: `training_allowed=false`, `rights_status=unknown`, `tenant_scope=restricted`; отсутствие любого поля означает reject.
- **[VERIFIED FACT]** License gate хранит source terms, acquisition method, jurisdiction, permitted purpose, attribution/notice obligations и юридическое evidence.
- **[VERIFIED FACT]** PII gate блокирует direct identifiers и sensitive attributes до удаления либо доказанного lawful basis.
- **[VERIFIED FACT]** Secrets gate блокирует credentials, private keys, tokens, internal endpoints и exploitable configuration; найденный working secret инициирует incident workflow.
- **[VERIFIED FACT]** Dedup выполняется до tokenization и после normalization: exact hashes, MinHash/LSH, semantic clusters; для code/config дополнительно AST, symbol, patch и repository ancestry fingerprints.
- **[VERIFIED FACT]** Contamination gate сравнивает source/provenance groups с sealed pretrain и posttrain eval registries; совпадение блокирует всю connected family до adjudication.
- **[RISK]** Автоматическая санация не доказывает права на использование и не превращает restricted source в trainable source.

## Quality и lineage

- **[VERIFIED FACT]** Каждый документ имеет object ID, source record, rights record, sensitivity, transformations, dedup cluster, contamination decision, quality vector, tokenizer version и final disposition.
- **[ENGINEERING HYPOTHESIS]** Quality sampling должен сочетать deterministic filters, small classifiers и blinded human audits по source/domain strata.
- **[EXPERIMENT REQUIRED]** Thresholds качества и downsampling калибруются на proxy loss и capability deltas, а не на эстетические оценки.
- **[VERIFIED FACT]** Snapshot manifest фиксирует ordered shard hashes, accepted token count по tokenizer candidate, source/domain/language mix, exclusions, tool versions и signatures.

## Tenant boundary

- **[VERIFIED FACT]** Сырые или sanitized данные enterprise tenant не входят в general PretrainCorpus по умолчанию.
- **[VERIFIED FACT]** Explicit opt-in не даёт автоматического допуска: нужны rights, privacy, secrets, contamination, de-identification и independent approval; raw object остаётся tenant-bound.
- **[VERIFIED FACT]** Train jobs читают только signed general snapshots через dedicated service identity; direct tenant namespace access запрещён.
- **[RISK]** Tenant-derived corpus может сохранять topology, business logic и уникальные события даже после удаления имён.

## Freeze evidence

- **[EXPERIMENT REQUIRED]** Corpus freeze требует: reproducible Merkle root; rights coverage report; PII/secrets residual audit; dedup report; contamination report; token counts по tokenizer; HYBRID-MIX manifest; deletion/impact drill; независимую выборочную проверку.
- **[VERIFIED FACT]** До появления подписанного bundle статус PretrainCorpus — `CANDIDATE / NOT FROZEN`.
