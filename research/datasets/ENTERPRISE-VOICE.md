# Enterprise Voice dataset contract

## Scope и источники

Status reports, executive summaries, incident updates, customer replies, risk memos, handoffs, escalation notes и decision records. Источники: NULLXES-authored templates, licensed/public communications, human-written scenarios и synthetic drafts с human review.

- **VERIFIED FACT:** Enterprise Voice обучает точности, evidence binding, audience adaptation и explicit uncertainty, а не декоративному «корпоративному тону».
- **VERIFIED FACT:** Private email, chat и tickets клиента запрещены для general training по умолчанию.
- **RISK:** Псевдонимизированная переписка может сохранять уникальные события и identities.

## Controls

- **VERIFIED FACT:** Rights/consent на текст, attachments и quoted content проверяются отдельно.
- **VERIFIED FACT:** PII/secret scan покрывает людей, клиентов, contracts, finances, incident identifiers, URLs и metadata; high-risk samples требуют human privacy review.
- **ENGINEERING HYPOTHESIS:** Dedup применяет exact hash, MinHash, claim/evidence/audience triples и отдельную кластеризацию templates.
- **EXPERIMENT REQUIRED:** Contamination scan использует topic/event/time/source split, semantic matching claims и shared evidence IDs с hidden eval.

## Quality gate

**VERIFIED FACT:** Каждое утверждение связано с evidence либо помечено как hypothesis/unknown; audience, required action, owner, deadline и risk корректны; fabricated status, hidden uncertainty и disclosure beyond permissions запрещены. Human reviewer подтверждает high-impact customer/incident examples.

## Mix и lineage

- **ENGINEERING HYPOTHESIS:** 65% synthetic human-reviewed / 35% human-authored licensed samples; high-impact messages — 100% human-reviewed.
- **EXPERIMENT REQUIRED:** Измерить factuality и escalation calibration отдельно от stylistic preference.
- **VERIFIED FACT:** Lineage хранит source rights, audience class, sensitivity, claims-to-evidence map, redactions, generator/teacher, reviewer, rubric scores и contamination fingerprints.
