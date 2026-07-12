# ADR-0003: World Model V0 предшествует learned V1

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Область: Organizational World Model.

## Контекст

- **VERIFIED FACT:** Learned transition model требует state/action/outcome traces с authoritative observations, provenance и policy context.
- **RISK:** Без V0 такие labels будут self-reported моделью, неполными и причинно неоднозначными.
- **ENGINEERING HYPOTHESIS:** Graph + event ledger + policy engine дают полезный runtime baseline и data collection substrate без второго LLM.

## Решение

- **VERIFIED FACT:** Сначала реализуется V0: typed state graph, immutable event ledger, deterministic policy engine и reconciliation.
- **VERIFIED FACT:** V1 1.5–3B допускается только после data-readiness review и работает сначала в shadow mode.
- **VERIFIED FACT:** Ни V0, ни V1 не обходят source-system authority, approval или tool gateway.

## Последствия

- **VERIFIED FACT:** V0 остаётся fallback и ground-truth interface даже после V1.
- **ENGINEERING HYPOTHESIS:** V1 фокусируется на delta/risk/reversibility/evidence prediction, а не на open-ended corporate memory.
- **RISK:** V0 ontology может переусложниться; новые entity types требуют measured task need.
- **EXPERIMENT REQUIRED:** V1 принимается только при улучшении critical-risk recall/missing-evidence detection против deterministic и structured ML baselines при заданном escalation budget.

## Stop condition

- **RISK:** Недостаточная trace quality, poor calibration, privacy leakage или отсутствие incremental utility останавливают V1 без блокировки E-01 V0.
