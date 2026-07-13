# ADR-0006: Direct 480B Instruct foundation

- **VERIFIED FACT:** Статус: Superseded by ADR-0007.
- **VERIFIED FACT:** Дата принятия: 2026-07-13.
- **VERIFIED FACT:** Дата supersession: 2026-07-13.

## Решение

- **VERIFIED FACT:** Прямой foundation LÆTEX E-01 — `Qwen/Qwen3-Coder-480B-A35B-Instruct`.
- **VERIFIED FACT:** `Qwen/Qwen3-Coder-Next-Base` 80B/3B не является foundation E-01 и сохраняется только как исторически отвергнутая или альтернативная research branch.
- **ENGINEERING HYPOTHESIS:** Broad CPT выключен по умолчанию, потому что upstream уже прошёл post-training и продолжение общего LM objective создаёт риск потери instruction/tool alignment.
- **EXPERIMENT REQUIRED:** Узкий DAPT допустим только как отдельно одобренная disabled-by-default ablation после frozen S0 baseline; он не создаёт parent канонического lineage.
- **VERIFIED FACT:** Тот же foundation checkpoint исключён из роли teacher. Любой будущий critic обязан быть отдельным checkpoint с собственными pin, lineage, H200 budget и approval.
- **ENGINEERING HYPOTHESIS:** Канонический lineage: `S0 → A1 → M1 → A2 → M2 → A3 → M3 → A4 → M4 → FP8`.
- **VERIFIED FACT:** `A1..A4` — retained training adapters; `M1..M4` — отдельные immutable BF16 merge artifacts; FP8 — только serving derivative от M4 после parity.
- **VERIFIED FACT:** Все model workloads, включая training, merge, evaluation, conversion и serving qualification, выполняются только на RunPod NVIDIA H200. Локальный control plane не хранит веса и не исполняет model workloads.
- **EXPERIMENT REQUIRED:** Multi-node allocation допускается только после provider attestation фактической fabric/topology и NCCL acceptance; наличие InfiniBand заранее не заявляется.

## Последствия

- **VERIFIED FACT:** Последовательность jobs: frozen `S0` → identity/tool train `A1` → BF16 merge `M1` → Action SFT train `A2` → BF16 merge `M2` → preference train `A3` → BF16 merge `M3` → GRPO train `A4` → BF16 merge/evaluation `M4` → отдельный FP8 conversion/parity/export.
- **RISK:** Train и merge нельзя объединять в один профиль: потеря retained adapter, parent hash или merge recipe делает lineage непроверяемым.
- **RISK:** FP8 не может быть training/merge parent или частью M4 BF16 artifact.

## Supersession

- **VERIFIED FACT:** Этот ADR заменяет более ранние предположения о foundation E-01, включая выбор 80B checkpoint, разделение 80B student/480B teacher и broad CPT как default phase.
- **VERIFIED FACT:** ADR-0005 не отменён: он остаётся политикой только для возможного будущего offline critic и не определяет foundation E-01.
- **VERIFIED FACT:** ADR-0007 впоследствии заменил этот ADR и принял independent from-scratch E-01 без внешнего weight parent.
- **VERIFIED FACT:** Qwen-derivative lineage из этого документа является историческим и не санкционирует training, initialization, merge или release canonical E-01.
