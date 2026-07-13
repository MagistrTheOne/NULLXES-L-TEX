# ADR-0007: Independent from-scratch E-01

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Дата: 2026-07-13.
- **VERIFIED FACT:** Область: canonical foundation decision для LÆTEX E-01.

## Контекст

- **VERIFIED FACT:** Предыдущее решение ADR-0006 определяло E-01 как derivative от внешнего checkpoint.
- **RISK:** Внешний weight parent ограничивает архитектурную независимость, tokenizer ownership, control над pretraining lineage и свободу исследования внутренних MoE/attention решений.
- **RISK:** Независимый pretraining резко увеличивает dataset, systems, H200, validation, schedule и capital risk; принятое решение не является доказательством выполнимости.

## Решение

- **VERIFIED FACT:** LÆTEX E-01 проектируется и обучается from scratch без внешнего weight parent, checkpoint initialization или inherited tokenizer.
- **ENGINEERING HYPOTHESIS:** Target: 64 layers, `d_model=8192`, GQA `64Q/8KV`, head dimension 128, hybrid attention `7 local : 1 global`, local window 16 384, 144 routed experts + 1 shared expert, Top-6, expert `d_ff=2048`, vocabulary 128K, context target 262 144 и BF16 master.
- **EXPERIMENT REQUIRED:** Estimates `~478.9B total / ~34.4B active` остаются provisional до executable parameter-count proxy и фиксации MoE placement, shared-expert accounting, embedding tying и attention implementation.
- **VERIFIED FACT:** Канонический lineage начинается с corpus/tokenizer artifacts и random initialization, а не с model weights третьей стороны.
- **VERIFIED FACT:** Все model workloads выполняются только на NVIDIA H200 HGX; локальная машина остаётся control/documentation plane без weights и training workloads.

## Consequences

- **VERIFIED FACT:** ADR-0006 superseded; ADR-0001 superseded отдельным ADR-0008.
- **VERIFIED FACT:** Qwen может существовать только за firewall ADR-0009 как benchmark и опциональный offline synthetic teacher, но не weight parent.
- **EXPERIMENT REQUIRED:** Architecture freeze требует proxy scaling, convergence, MoE balance, kernel feasibility, long-context curriculum и H200 communication evidence.
- **RISK:** Full-scale pretraining запрещён до прохождения proxy, data-readiness, systems-recovery, topology и budget gates.

## Acceptance

- **EXPERIMENT REQUIRED:** Proxy должен подтвердить parameter accounting, stable routing, отсутствие sustained divergence, checkpoint recovery и scale-transfer assumptions.
- **EXPERIMENT REQUIRED:** Независимость lineage подтверждается manifest, в котором отсутствуют external checkpoint hashes в parent graph.
- **RISK:** Если H200 economics, licensed token supply или scale transfer не проходят gate, решение возвращается на review; silent substitution внешнего checkpoint запрещён.
