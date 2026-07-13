# ADR-0009: Qwen reference/teacher firewall

- **VERIFIED FACT:** Статус: Accepted.
- **VERIFIED FACT:** Дата: 2026-07-13.
- **VERIFIED FACT:** Область: все E-01 data, evaluation и lineage paths.

## Решение

- **VERIFIED FACT:** Qwen не является weight parent, initialization source, tokenizer source, runtime dependency или canonical component E-01.
- **VERIFIED FACT:** Qwen разрешён как внешний benchmark и как опциональный offline synthetic teacher только на NVIDIA H200.
- **VERIFIED FACT:** Teacher generation не входит в live runtime, policy decision, approval path или authoritative world state.
- **ENGINEERING HYPOTHESIS:** Synthetic samples могут использоваться только как quarantined candidate data после license/provenance review, contamination checks, executable verification и quality filtering.

## Firewall

- **VERIFIED FACT:** Teacher manifest хранится отдельно от scratch model lineage и содержит exact model/revision, license snapshot, generation config, prompts, hashes, H200 run identity и accept/reject reasons.
- **VERIFIED FACT:** External model output никогда не считается ground truth; high-risk samples требуют independent verifier и human review.
- **VERIFIED FACT:** Benchmark tasks и teacher-generation prompts не пересекаются с private evaluation holdouts.
- **RISK:** Teacher data может переносить identity, style, factual errors, unsafe tool patterns и benchmark contamination.
- **EXPERIMENT REQUIRED:** Ablation `human/verified data only` против `+ teacher candidates` должна показать statistically defensible uplift без identity leakage, safety regression или contamination.
- **RISK:** При отсутствии uplift teacher budget прекращается; Qwen не получает новый статус в lineage.

## Relation to prior decisions

- **VERIFIED FACT:** Этот ADR уточняет ADR-0005 для independent E-01 и отменяет любые его формулировки, где Qwen назван direct foundation.
