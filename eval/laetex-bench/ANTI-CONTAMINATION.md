# Anti-contamination contract

## Registry separation

- **[VERIFIED FACT]** Pretrain Capability и Posttrain Enterprise Action используют отдельные sealed registries и denylist roots.
- **[VERIFIED FACT]** PretrainCorpus, posttrain datasets, synthetic-generator inputs, retrieval indexes и grader context проверяются против обоих registries.
- **[VERIFIED FACT]** Sample-level eval feedback не возвращается ни в HYBRID-MIX, ни в posttrain curriculum.
- **[RISK]** Public benchmark contamination может существовать до начала программы; такие suites маркируются diagnostic-only и не используются как единственный gate.

## Split policy

**[VERIFIED FACT]** Hidden evaluation одновременно применяет:

1. **VERIFIED FACT — Time split:** source/event/commit после frozen cutoff.
2. **VERIFIED FACT — Repository split:** forks, mirrors, templates, shared commit ancestry и generated variants объединены в одну group.
3. **VERIFIED FACT — Organization split:** artifacts, conventions, topology и communications одной organization family не пересекают train/eval.

**VERIFIED FACT:** Три ограничения применяются совместно, а не как альтернативы.

## Detection

- **ENGINEERING HYPOTHESIS:** Exact SHA-256 покрывает canonical content, commits, diffs и evidence.
- **ENGINEERING HYPOTHESIS:** MinHash/LSH token shingles выявляет near-duplicates.
- **ENGINEERING HYPOTHESIS:** Semantic embeddings выявляют paraphrased issue, task, solution и communication.
- **ENGINEERING HYPOTHESIS:** Normalized AST, symbol/data-flow и patch fingerprints покрывают код/config.
- **ENGINEERING HYPOTHESIS:** Provenance graph связывает forks, teacher generations, templates, incidents и derived tasks.
- **EXPERIMENT REQUIRED:** Canary strings и task-specific probes применяются для memorization audit.

## Sealing и доступ

**VERIFIED FACT:** Hidden payloads хранятся в отдельном encrypted namespace; model/data developers не имеют read access. Harness выдаёт ephemeral task instance, принимает action log и возвращает агрегированные результаты. Task manifests, graders и access events подписываются и audit-logged.

- **VERIFIED FACT:** Обнаруженный train↔hidden match блокирует task family до adjudication; тихое удаление только совпавшей строки недостаточно.
- **VERIFIED FACT:** Synthetic paraphrase hidden task contaminated, если generator видел train solution или исходный protected task.
- **VERIFIED FACT:** Eval feedback с solution-level detail не возвращается training pipeline.
- **RISK:** Semantic thresholds дают false positives/negatives; спорные clusters проверяются blinded reviewers.

## Release audit

**VERIFIED FACT:** До unblinding независимый data steward подписывает split manifest и contamination report. После оценки публикуются counts exact/near/semantic/AST matches, exclusions и regenerated families без раскрытия hidden content.

- **ENGINEERING HYPOTHESIS:** Rotating hidden families и delayed time windows снизят adaptive overfitting.
- **EXPERIMENT REQUIRED:** Red-team leakage через logs, caches, teacher prompts, retrieval indexes, model-based grader traces и human annotation tools.
