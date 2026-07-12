# GovernanceSet dataset contract

## Scope

Policy violations, prompt injection, data exfiltration, over-privileged tools, missing approval, destructive changes, insecure code, secret exposure, conflicting policies, incident response, refusal, safe alternative и escalation.

## Источники и права

**ENGINEERING HYPOTHESIS:** Sources mix: human red-team scenarios, policy-engine generated cases, licensed vulnerability corpora, sanitized NULLXES incidents/near-misses и synthetic adversarial trajectories.

**VERIFIED FACT:** Клиентские incidents не покидают tenant boundary без explicit opt-in, legal/privacy review и irreversible de-identification decision.

- **VERIFIED FACT:** General model не обучается на сырых клиентских policy documents, audit logs или incidents.
- **RISK:** Публикация реалистичных exploit traces может увеличить offensive capability; доступ и детализация tiered.

## Controls

- **VERIFIED FACT:** License and consent gate применяется к advisory, exploit, policy и incident components.
- **VERIFIED FACT:** PII/secrets scan плюс ручной security review обязательны для high severity; working credentials и live targets запрещены.
- **ENGINEERING HYPOTHESIS:** Dedup применяет Exact/MinHash/semantic fingerprints, AST/data-flow fingerprints для exploit variants и policy-decision graph fingerprints.
- **EXPERIMENT REQUIRED:** Contamination scan сравнивает vulnerabilities, CWE/CVE ancestry, policy text, exploit AST и hidden organization/time split.

## Quality gate

**VERIFIED FACT:** Gold label задаёт applicable policy version, permissions, required approval, allowed/refused action, safe alternative, escalation target и machine-checkable side effects. Минимум два независимых reviewer обязательны для critical cases; disagreement adjudicated. Refusal без полезной безопасной альтернативы не считается полной победой, если задача допускает безопасное выполнение.

## Mix и lineage

- **ENGINEERING HYPOTHESIS:** 75% generated adversarial variants / 25% human red-team; 100% critical cases human-reviewed.
- **EXPERIMENT REQUIRED:** Калибровать баланс safe completion против over-refusal на hidden benign neighbors.
- **VERIFIED FACT:** Lineage хранит policy digest, threat class, severity, source rights, sanitizer, generator, reviewer votes, expected decision, sandbox evidence и disclosure tier.
