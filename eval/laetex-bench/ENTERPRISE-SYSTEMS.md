# Track 2: Enterprise Systems & Integration

## Tasks

API integration, schema evolution, event contract, IAM-safe wiring, IaC change, Kubernetes deployment, migration/rollback, SLO/runbook update, incident diagnosis и architecture plan с executable checks.

## Grading

- **VERIFIED FACT:** Automatic grading: schema/contract tests, plan/apply in sandbox, policy-as-code, dependency resolution, migration reversibility, telemetry assertions, SLO checks и state-delta comparison.
- **VERIFIED FACT:** Model-based grading оценивает trade-off completeness и architecture coherence только как secondary score.
- **VERIFIED FACT:** Human review покрывает ADR quality, operational realism, risk prioritization и stakeholder constraints.
- **VERIFIED FACT:** Security checks покрывают least privilege, secret handling, network boundaries, supply chain, unsafe migration и data residency.

## Metrics

VETCR, integration contract pass rate, predicted-vs-observed delta accuracy, rollback success, policy compliance, missing-evidence detection, time/cost-to-verified-state и incident recovery rate.

## Replayability и splits

**VERIFIED FACT:** Environment topology, images, API fixtures, clocks, failure injection, policy bundles и telemetry streams pinned. Hidden splits разделены по system family, vendor/API version, organization topology и time; variants одной reference architecture не пересекают splits.

- **VERIFIED FACT:** Valid configuration text без успешного sandbox validation не является completion.
- **VERIFIED FACT:** Неодобренное изменение IAM, network или production-like state обнуляет score.
- **ENGINEERING HYPOTHESIS:** Track требует ≥450 hidden tasks, включая ≥100 controlled failure/recovery.
- **EXPERIMENT REQUIRED:** Калибровать realism gap между emulator и production-like staging.
- **RISK:** Vendor mocks могут скрыть rate limits и eventual consistency; contract/replay suite обязан моделировать оба класса.
