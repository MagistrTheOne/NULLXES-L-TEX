# Independent E-01 — top-10 risk register

## Управление

- **[VERIFIED FACT]** P0 не принимается; P1 требует Program Owner decision; каждый closure ссылается на signed evidence.
- **[EXPERIMENT REQUIRED]** Никакой риск не считается закрытым по плану или vendor claim.

## R-01 — tokenizer failure

- **[RISK]** Плохая compression, Unicode/byte handling или code tokenization увеличит training/inference cost и необратимо ограничит capability.
- **[EXPERIMENT REQUIRED]** Multi-domain fertility, fallback, round-trip и 1B/7B ablation.
- **[VERIFIED FACT]** Mitigation: два candidates, frozen regression corpus, freeze до 30B; owner — Research Lead.

## R-02 — data rights

- **[RISK]** Unknown/incompatible rights могут сделать corpus и checkpoint юридически непригодными.
- **[EXPERIMENT REQUIRED]** Independent rights sampling audit и snapshot coverage report.
- **[VERIFIED FACT]** Mitigation: source allowlist, purpose-specific rights, default deny, impact deletion; owner — Data Lead/Legal.

## R-03 — router collapse

- **[RISK]** MoE routing может концентрироваться на малом числе experts, терять domain specialization или dropping tokens.
- **[EXPERIMENT REQUIRED]** 1B/7B/30B utilization, entropy, imbalance, domain concentration и failure injection.
- **[VERIFIED FACT]** Mitigation: load-balancing controls, capacity monitoring, dense control, stop on collapse; owner — Research Lead.

## R-04 — hybrid-attention cost/quality failure

- **[RISK]** Hybrid attention может не дать kernel speedup либо потерять distant dependencies.
- **[EXPERIMENT REQUIRED]** Matched full-attention controls по loss, long-context tasks, memory, throughput и MFU.
- **[VERIFIED FACT]** Mitigation: staged context curriculum и запрет 128K–256K claim без gate; owner — Architecture Lead.

## R-05 — low MFU

- **[RISK]** Communication, routing, pipeline bubbles, data stalls или long-context kernels могут сделать H200 economics неприемлемой.
- **[EXPERIMENT REQUIRED]** Measured per-stage MFU/throughput на exact topology, включая checkpoint overhead.
- **[VERIFIED FACT]** Mitigation: topology profiling, bucketed sequences, PP/EP/TP tuning, budget kill floor; owner — Platform Lead.

## R-06 — checkpoint recovery failure

- **[RISK]** Неполный distributed checkpoint или untested resharding может потерять многодневный run.
- **[EXPERIMENT REQUIRED]** Node-failure, restore, reshard и deterministic continuity drills на proxies и 30B.
- **[VERIFIED FACT]** Mitigation: transactional manifests, frequent async checkpoints, isolated object storage, restore before promotion; owner — Platform Lead.

## R-07 — 512/1024 H200 capacity unavailable

- **[RISK]** Provider может не подтвердить однородную capacity, fabric, reservation window или failure-domain SLA.
- **[EXPERIMENT REQUIRED]** Signed reservation/topology attestation и NCCL/storage acceptance на allocation class.
- **[VERIFIED FACT]** Mitigation: target run запрещён без capacity contract; нельзя заменять mixed GPUs или дробными unattested clusters; owner — Program Owner.

## R-08 — contamination

- **[RISK]** Train/eval overlap через forks, synthetic derivations, public benchmarks, grader context или feedback создаст ложное capability evidence.
- **[EXPERIMENT REQUIRED]** Exact/near/semantic/AST/provenance scans и memorization probes до каждого freeze.
- **[VERIFIED FACT]** Mitigation: sealed registries, family-level quarantine, no solution feedback, independent steward; owner — Evaluation Lead.

## R-09 — budget overrun / invalid scaling economics

- **[RISK]** `4–6T` target и 512/1024 H200 могут не окупаться даже при технической сходимости.
- **[EXPERIMENT REQUIRED]** 1B/7B/30B scaling fit, tokens-to-quality curve, MFU, checkpoint/network overhead и sensitivity model.
- **[VERIFIED FACT]** Mitigation: 30B mandatory gate, budget-at-risk cap, stop conditions, no target reservation on narrative forecasts; owner — Program Owner.

## R-10 — native identity or posttrain governance failure

- **[RISK]** Third-party persona leakage, fabricated execution, policy bypass или action overfitting могут появиться после posttraining.
- **[EXPERIMENT REQUIRED]** `0/10 000` persona suite, four-track action eval, capability retention и FP8 parity.
- **[VERIFIED FACT]** Mitigation: NATIVE-IDENTITY contract, external deny-by-default policy engine, stage gates, BF16 rollback; owner — Safety & Governance Lead.

## Escalation

- **[VERIFIED FACT]** Data-rights, tenant isolation, contamination или destructive policy P0 немедленно останавливает snapshot promotion и training.
- **[RISK]** Снижение severity без нового evidence запрещено.
