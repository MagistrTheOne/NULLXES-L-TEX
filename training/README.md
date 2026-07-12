# LÆTEX E-01: training program

## Неподвижные ограничения

- **[VERIFIED FACT]** Порядок gate-ов: Phase 0 Baseline → Phase 1 CPT → Phase 2 SFT → Phase 3 Preference → Phase 4 GRPO → Phase 5 Router/World Model → Phase 6 Release.
- **[VERIFIED FACT]** Compute — только NVIDIA H200 SXM 141 GB в RunPod Secure Cloud; multi-node — H200 Instant Clusters.
- **[VERIFIED FACT]** Локальная машина не получает веса и не выполняет inference/training/teacher generation.
- **[VERIFIED FACT]** RunPod Network Volume — рабочий набор; external encrypted object store — durable registry и source of truth.
- **[VERIFIED FACT]** Qwen3-Coder-480B-A35B-Instruct используется только offline и никогда не является live runtime.
- **[RISK]** Следующая фаза не стартует по календарю: нужен подписанный gate artifact предыдущей фазы.

## Gate sequence

| Фаза | Решение | Обязательный выход |
|---|---|---|
| 0 | **[EXPERIMENT REQUIRED]** Зафиксировать baseline и стоимость. | Frozen eval manifest, VETCR baseline, replay bundle. |
| 1 | **[EXPERIMENT REQUIRED]** CPT только при доказанном domain gain без coding regression. | Resumable CPT checkpoint и lineage. |
| 2 | **[EXPERIMENT REQUIRED]** Сформировать LÆTEX behavior/tool contract. | SFT adapter bundle и identity report. |
| 3 | **[EXPERIMENT REQUIRED]** Улучшить выбор безопасных проверяемых действий. | Preference checkpoint и pair audit. |
| 4 | **[EXPERIMENT REQUIRED]** Доказать, что executable RL лучше дополнительного SFT. | GRPO policy и replayable trajectories. |
| 5 | **[EXPERIMENT REQUIRED]** Обучить router; World Model V1 только если лучше V0. | Router, audit mapping, calibrated transition model либо documented no-go. |
| 6 | **[EXPERIMENT REQUIRED]** Выпустить или отклонить frozen candidate. | Signed evidence bundle и release decision. |

## Method policy для E-01

- **[ENGINEERING HYPOTHESIS]** E-01: selective CPT + BF16 LoRA/adapters для SFT/preference/GRPO, с replay mix и immutable base/CPT reference.
- **[RISK]** QLoRA не является default: 4-bit quantization hybrid DeltaNet/MoE path должна отдельно доказать kernel correctness и отсутствие quality loss.
- **[RISK]** Full fine-tuning всех 80B parameters имеет высокий optimizer/checkpoint cost; допускается только после selective-tuning ablation.
- **[ENGINEERING HYPOTHESIS]** Selective MoE tuning ограничивается shared experts, attention/DeltaNet projections, norms и контролируемой частью router parameters; routed expert weights размораживаются только по доказанному bottleneck.
- **[RISK]** Adapter merge не является автоматическим release step. Merge принимается только при bitwise/config compatibility и полном повторном eval.
- **[VERIFIED FACT]** Distillation и teacher-student labels генерируются offline; teacher outputs не считаются ground truth без tests, policy checks или human adjudication.
- **[ENGINEERING HYPOTHESIS]** Full-parameter independent pretraining, новый tokenizer и собственная foundation architecture откладываются в LÆTEX-2.

## Reproducibility contract

Каждый run manifest обязан содержать:

- **[VERIFIED FACT]** Git commit, image digest, profile hash, base checkpoint hash, tokenizer hash и dataset manifest hash.
- **[VERIFIED FACT]** World size, TP/PP/EP/CP/DP, precision, seeds, optimizer/scheduler, global batch и sequence-length distribution.
- **[VERIFIED FACT]** RunPod allocation ID, region/datacenter, Network Volume ID (без credentials), start/stop timestamps и aggregated cost.
- **[VERIFIED FACT]** Checkpoint inventory, resume-test result, metric definitions, grader versions и promotion decision.
- **[RISK]** Private held-out tasks хранятся отдельно от training namespaces и не появляются в prompts teacher-generation jobs.

## Wall-clock и стоимость

- **[ENGINEERING HYPOTHESIS]** Все сроки в phase files — planning ranges, не benchmark results.
- **[EXPERIMENT REQUIRED]** После smoke/pilot пересчитать сроки из observed tokens/s, rollout throughput, failure rate и checkpoint overhead.
- **[RISK]** Экономическое решение принимается по cost per incremental verified task, а не по loss alone или GPU-hour utilization.

