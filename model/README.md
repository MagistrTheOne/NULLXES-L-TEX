# Lineage независимой LÆTEX E-01

**[VERIFIED FACT]** Каноническая E-01 в этом каталоге — новая decoder-only MoE
foundation, обучаемая с нулевой инициализации собственных weights и собственного
tokenizer. Ни один внешний checkpoint не является родителем target lane.

**[VERIFIED FACT]** Все manifests имеют `status: planned`,
`execution_state: not_run`: они не создают RunPod-инфраструктуру и не заявляют
выполненное обучение.

## Две непересекающиеся линии

- **Proxy lane:** `PX1-1B → PX2-7B → PX3-30B → ARCH-FREEZE`. Proxy checkpoints
  проверяют tokenizer, data loader, initialization, scaling, routing, kernels,
  checkpoint/resume и quality-per-compute.
- **Target lane:** `T0-TOKENIZER → D0-CORPUS → I0-INIT → P0-PRETRAIN-8K →
  LC32K → LC128K → LC256K → SFT → PREF → GRPO → R1-BF16 → FP8`.

**[VERIFIED FACT]** Proxy weights никогда не копируются, не расширяются и не
используются как target parent. `ARCH-FREEZE` переносит только подписанную
спецификацию и измеренные hyperparameter/scaling decisions. `I0-INIT` создаёт
target weights заново из зафиксированного seed и initialization contract.

## Architecture freeze

**[ENGINEERING HYPOTHESIS]** Target topology исследует 144 routed experts;
`EP=16` даёт ровно 9 routed experts на rank. Точные layer count, hidden size,
shared expert, active/total parameter counts, attention schedule, optimizer,
token budget и μP transfer считаются незакреплёнными до `ARCH-FREEZE`.

**[RISK]** Одновременная независимая декомпозиция `TP8×PP8×EP16` уже требует
world size 1024 при `CP=DP=1`. Поэтому 512 H200 — минимальный campaign envelope,
но не доказательство, что exact target topology помещается на 512. Профили
фиксируют валидные phase-specific fallback-разложения; подмена арифметики
запрещена.

## Execution invariants

- **[VERIFIED FACT]** Только NVIDIA H200; target planning: 512 minimum, 1024
  recommended. Локально разрешён только control plane без weights/datasets/train.
- **[RISK]** До reservation обязательны provider-attested NVLink/NVSwitch внутри
  HGX-узла, InfiniBand между узлами и acceptance NCCL/all-to-all/checkpoint.
- **[VERIFIED FACT]** External encrypted versioned object store — source of truth.
  RunPod Network Volume и node scratch — только working/cache layers.
- **[ENGINEERING HYPOTHESIS]** Любые wall-clock, throughput, MFU, token-budget и
  cost значения остаются гипотезами до proxy и target pilots.
- **[VERIFIED FACT]** BF16 `R1` — release master. FP8 — inference-only derivative,
  никогда не training parent.

## Historical derivative branch

Предыдущие derivative stage contracts выведены из canonical namespace и
инвентаризированы в
[`historical/qwen-derivative-e01/MANIFEST.yaml`](historical/qwen-derivative-e01/MANIFEST.yaml).
Канонический architecture contract target lane:
[`latex-e01-480a35.yaml`](latex-e01-480a35.yaml)
(`provenance.weight_parent: null`, independent random init).
