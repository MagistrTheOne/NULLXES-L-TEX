# Context curriculum contract

## Принцип

- **[VERIFIED FACT]** Target context capability нельзя считать полученной из одного config value; она требует native training stages, data packing, position strategy, kernels и held-out evaluation.
- **[ENGINEERING HYPOTHESIS]** Pretraining начинается на коротком/среднем context для compute efficiency и расширяется по evidence-gated stages.
- **[RISK]** Раннее обучение всего `4–6T` budget на максимальной длине резко увеличит attention FLOPs и снизит data throughput.

## Candidate stages

1. **[ENGINEERING HYPOTHESIS]** `C0: 4K` — architecture/tokenizer/data smoke и bulk early proxy pretraining.
2. **[ENGINEERING HYPOTHESIS]** `C1: 8K` — stable bulk stage с document-boundary packing.
3. **[ENGINEERING HYPOTHESIS]** `C2: 16K–32K` — repository/system documents, multi-file code и dependency evidence.
4. **[ENGINEERING HYPOTHESIS]** `C3: 64K` — native long-context continuation после short-context non-inferiority.
5. **[EXPERIMENT REQUIRED]** `C4: 128K–256K` допускается только после hybrid-attention kernel, memory, quality и cost evidence; это не обещанный E-01 capability.

## Gates между стадиями

- **[EXPERIMENT REQUIRED]** Каждая стадия проходит convergence continuity, short-context retention, length-stratified perplexity, retrieval/needle, multi-hop code dependency, position extrapolation, throughput/MFU и checkpoint restore.
- **[VERIFIED FACT]** Stage manifest фиксирует sequence distribution, packing algorithm, RoPE/position parameters, attention pattern, CP/SP topology, optimizer transition и token budget.
- **[RISK]** Synthetic long documents и repeated padding могут дать формальный context length без полезной cross-document reasoning.
- **[RISK]** Hybrid local/global attention может экономить FLOPs, но потерять distant dependency information; full-attention control обязателен на proxies.

## Data constraints

- **[VERIFIED FACT]** Связанные files/events сохраняют causal order и provenance; unrelated records нельзя склеивать так, чтобы модель учила ложные зависимости.
- **[VERIFIED FACT]** Train/eval split наследуется на уровне repository, organization, event и derivation family независимо от chunking.
- **[EXPERIMENT REQUIRED]** Long-context mixture и stage token fractions выбираются по proxy ablation, а не фиксируются как факт.
