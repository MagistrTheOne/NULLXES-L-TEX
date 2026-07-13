# HYBRID-MIX contract

## Контракт смеси

- **[VERIFIED FACT]** HYBRID-MIX — versioned policy, которая отображает approved PretrainCorpus objects в sampling weights; это не статический список процентов.
- **[ENGINEERING HYPOTHESIS]** Начальный candidate диапазон: `40–55%` high-quality natural language, `25–35%` code, `8–15%` math/STEM, `5–10%` structured enterprise/system artifacts, `5–15%` multilingual material; диапазоны перекрываются только на этапе design и должны быть нормализованы в каждом manifest.
- **[EXPERIMENT REQUIRED]** Ни один процент не получает статус approved до 1B/7B proxy ablations; 30B proxy подтверждает выбранную смесь перед target approval.
- **[RISK]** Чрезмерный code weight способен улучшить узкие coding evals, но ухудшить language, planning, multilingual и safety substrate.

## Sampling invariants

- **[VERIFIED FACT]** Sampling unit — provenance group, а не отдельный document; fork, mirror, template и derived synthetic family не могут многократно усиливать один источник.
- **[VERIFIED FACT]** Каждый batch и checkpoint interval получает auditable realized mix по accepted tokens, sources, languages, domains и quality strata.
- **[VERIFIED FACT]** Source caps ограничивают крупнейший domain/source/organization cluster; значения caps замораживаются в manifest.
- **[VERIFIED FACT]** Synthetic data хранит generator, prompt, source inputs, verifier и derivation graph; synthetic descendants не пересекают eval families.
- **[ENGINEERING HYPOTHESIS]** Verified synthetic доля broad pretrain должна быть низкой по умолчанию и увеличиваться только при доказанном proxy gain без memorization или style collapse.

## Curriculum

- **[ENGINEERING HYPOTHESIS]** Early stage предпочитает clean, short/medium documents и стабильный language/code balance; поздние стадии увеличивают difficult code, math, systems artifacts и long-context packing.
- **[EXPERIMENT REQUIRED]** Сравнить static mix, staged curriculum и loss-aware reweighting при одинаковом token/compute budget.
- **[VERIFIED FACT]** Eval-driven reweighting использует только public/dev suites; sealed holdout не возвращает sample-level signal в mixer.
- **[RISK]** Dynamic reweighting по одному proxy benchmark создаёт скрытое benchmark overfitting.

## Promotion evidence

- **[EXPERIMENT REQUIRED]** Mix promotion требует domain loss curves, downstream capability deltas, tokenizer compression, duplicate exposure, memorization probes, router utilization для MoE proxies и cost/token.
- **[VERIFIED FACT]** Manifest фиксирует weights, caps, curriculum stages, RNG seeds, sampler code hash, snapshot IDs и expected token counts.
- **[VERIFIED FACT]** Любое изменение source eligibility, weight, cap или curriculum создаёт новый immutable mix version.
