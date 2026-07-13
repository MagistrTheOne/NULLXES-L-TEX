# LÆTEX Corpus: independent E-01 data program

## Разделение corpus planes

- **[VERIFIED FACT]** [PretrainCorpus](PRETRAIN-CORPUS.md) задаёт broad corpus независимого pretraining с нуля.
- **[VERIFIED FACT]** [HYBRID-MIX](HYBRID-MIX.md) задаёт sampling и curriculum policy поверх approved snapshots.
- **[VERIFIED FACT]** [Context curriculum](CONTEXT-CURRICULUM.md) задаёт evidence-gated увеличение sequence length.
- **[VERIFIED FACT]** CodeWorld, SystemWorld, Enterprise Voice, ActionWorld и GovernanceSet являются отдельными post-training/action наборами; их labels и hidden eval не смешиваются с broad pretrain автоматически.
- **[VERIFIED FACT]** Для любого объекта default — `training_allowed=false`; отсутствие rights, tenant scope или gate decision означает reject.

## Planning targets

- **[ENGINEERING HYPOTHESIS]** `4–6T` accepted tokens — planning range для target-scale PretrainCorpus, а не утверждённый бюджет и не выполненный результат.
- **[EXPERIMENT REQUIRED]** Target run получает approval только после 1B/7B/30B proxy scaling, mixture/context ablations, MFU/throughput evidence и budget review.
- **[ENGINEERING HYPOTHESIS]** Post-training candidate ranges: `180k–300k` verified examples, `60k–120k` executable trajectories и `20k–60k` failure/recovery trajectories.
- **[EXPERIMENT REQUIRED]** Все ranges уточняются power analysis, marginal-quality curves и стоимостью human/executable verification.

## Unified admission controls

**[VERIFIED FACT]** `ingest → quarantine → rights → PII/secrets → normalize → dedup → contamination → quality → purpose assignment → immutable snapshot`

1. **[VERIFIED FACT]** Licensing gate блокирует unknown, incompatible или unverifiable rights.
2. **[VERIFIED FACT]** Privacy/secrets gate блокирует unresolved PII, credentials, keys, private endpoints и tenant identifiers.
3. **[VERIFIED FACT]** Dedup использует exact, MinHash/LSH и semantic methods; code/config дополнительно AST, symbol, patch и ancestry fingerprints.
4. **[VERIFIED FACT]** Contamination связывает train/eval через provenance graph и блокирует connected family, а не только совпавшую строку.
5. **[VERIFIED FACT]** Tenant data default-denied для general pretrain/posttrain; explicit opt-in не обходит rights, privacy, security или contamination review.
6. **[RISK]** Semantic filters ошибаются в обе стороны; thresholds калибруются на размеченной выборке и хранятся по version.

## Storage и lineage

- **[VERIFIED FACT]** Raw quarantine, canonical objects, shards, manifests и verifier artifacts хранятся раздельно в encrypted immutable object storage.
- **[VERIFIED FACT]** Train workers читают только signed snapshots через purpose-scoped identity; прямой доступ к raw или tenant stores запрещён.
- **[VERIFIED FACT]** [Lineage schema](LINEAGE-SCHEMA.md) связывает source, rights, consent, transformations, tokenizer, dedup, contamination, split и checkpoint impact.
- **[VERIFIED FACT]** [Tenant isolation](TENANT-ISOLATION.md) определяет default-deny и explicit opt-in workflow.
- **[RISK]** Ни corpus volume, ни quality, ни proxy gains пока не измерены; документы задают contracts, а не заявляют эксперименты.
