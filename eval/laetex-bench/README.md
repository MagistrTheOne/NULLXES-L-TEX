# LÆTEX-Bench

## Два независимых evaluation planes

- **[VERIFIED FACT]** `Pretrain Capability` оценивает base-model learning, scaling, tokenizer, multilingual/language, code, math, knowledge, long context, MoE routing и memorization до action post-training.
- **[VERIFIED FACT]** `Posttrain Enterprise Action` сохраняет четыре трека: Repository Engineering, Enterprise Systems & Integration, Governance & Safe Execution, Corporate Digital Employee Communication.
- **[VERIFIED FACT]** Pretrain capability score не заменяет VETCR, а VETCR не доказывает качество base pretraining.
- **[RISK]** Сведение planes в один weighted score позволяет скрыть catastrophic regression.

## Pretrain Capability track

- **[EXPERIMENT REQUIRED]** Proxy suite измеряет validation loss по frozen corpus strata, scaling fit, downstream few-shot/zero-shot capability, tokenizer compression/fallback, code execution, math exactness, factual calibration и memorization.
- **[EXPERIMENT REQUIRED]** Context gates измеряют short-context retention, length-stratified loss, retrieval, multi-hop dependencies, long-code coherence, throughput и MFU на каждом context stage.
- **[EXPERIMENT REQUIRED]** MoE proxies публикуют expert utilization, load imbalance, dropped tokens, routing entropy и domain concentration.
- **[VERIFIED FACT]** 1B и 7B proxies используются для architecture/tokenizer/mix elimination; 30B proxy обязателен перед approval target-scale run.
- **[RISK]** Public academic benchmarks могут быть contaminated и используются только как secondary diagnostic; sealed capability sets и corpus overlap audit обязательны.

## Posttrain Enterprise Action tracks

- **[VERIFIED FACT]** Главный KPI — VETCR из [METRICS.md](METRICS.md).
- **[VERIFIED FACT]** Каждая task фиксирует state, goal, permissions, policy, tools, approvals, budget, invariants, verifier и prohibited effects.
- **[VERIFIED FACT]** Unauthorized side effect или completion claim без evidence обнуляет task score.
- **[VERIFIED FACT]** Four-track reports публикуются отдельно; governance critical failures не усредняются.

## Grading и replay

1. **[VERIFIED FACT]** Deterministic graders являются primary там, где доступны.
2. **[VERIFIED FACT]** Model graders — rubric-bound secondary signal и не переопределяют executable/policy failure.
3. **[VERIFIED FACT]** Human review покрывает ambiguity, high-impact communication и critical governance.
4. **[VERIFIED FACT]** Все checkpoints, tokenizer, corpus/eval manifests, runtime, seeds и graders content-addressed.

## Status

- **[VERIFIED FACT]** `baseline-manifest.yaml` теперь является readiness/evidence schema независимой E-01, а не manifest parent checkpoint.
- **[EXPERIMENT REQUIRED]** Thresholds, sample sizes и confidence methods замораживаются до сравнения candidates.
- **[RISK]** Никаких proxy, 30B, target или release результатов пока не заявлено.
