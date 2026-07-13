# Lineage модели LÆTEX E-01

**[VERIFIED FACT]** Этот каталог — канонический документационный manifest прямого
наследования LÆTEX E-01 от `Qwen/Qwen3-Coder-480B-A35B-Instruct`.

**[VERIFIED FACT]** Файлы каталога не создают инфраструктуру, не содержат
credentials и не утверждают, что training, merge, evaluation или release run
уже выполнялся.

## Канонические файлы

- `latex-e01-480a35.yaml` — identity модели, проверяемая upstream-архитектура,
  policy адаптации, context/runtime constraints и полный lineage.
- `stages/S0-UPSTREAM.yaml` — закрепление и верификация upstream как `S0`.
- `stages/S1-IDENTITY.yaml` — обучение и сохранение identity/tool adapter `A1`.
- `stages/M1-IDENTITY-MERGED.yaml` — BF16 merge только `A1` в `S0`.
- `stages/S2-ACTION-SFT.yaml` — обучение и сохранение Action SFT adapter `A2`.
- `stages/M2-ACTION-MERGED.yaml` — BF16 merge только `A2` в `M1`.
- `stages/S3-PREFERENCE.yaml` — обучение и сохранение preference adapter `A3`.
- `stages/M3-PREFERENCE-MERGED.yaml` — BF16 merge только `A3` в `M2`.
- `stages/S4-GRPO.yaml` — обучение и сохранение GRPO adapter `A4` от `M3`.
- `stages/M4-RELEASE.yaml` — BF16 merge только `A4` в `M3`.
- `stages/FP8-SERVING-DERIVATIVE.yaml` — отдельный FP8 conversion/export и parity только от immutable BF16 `M4`.
- `../infra/runpod/profiles/fp8-export.yaml` — отдельный FP8 serving derivative
  только от прошедшего gates BF16 `M4`.

## Lineage

**[VERIFIED FACT]** Обязательная последовательность train → verify → BF16 merge →
следующий train:

`S0 -> A1 -> M1 -> A2 -> M2 -> A3 -> M3 -> A4 -> M4 -> FP8 serving derivative`

**[VERIFIED FACT]** Training-стадии создают retained adapters `A1..A4`.
Merge-стадии не изменяют родителей: каждый merge пишет новый immutable BF16
artifact с новым SHA-256. После каждого merge следующий training-stage начинает
работу с новым optimizer/scheduler state.

## Обязательное закрепление

До любого training:

1. **[VERIFIED FACT]** Использовать только закреплённую Hugging Face revision
   `9d90cf8fca1bf7b7acca42d3fc9ae694a2194069`, проверенную через official API
   2026-07-13. Commit SHA не является SHA-256 hash весов.
2. **[EXPERIMENT REQUIRED]** На RunPod создать manifest всех обязательных
   файлов, размеров и SHA-256, включая все 241 weight shards, config, tokenizer
   и chat template; до этого training заблокирован.
3. **[EXPERIMENT REQUIRED]** На RunPod архивировать и хешировать upstream
   Apache-2.0 license и notices для exact revision.
4. **[VERIFIED FACT]** Получить точные имена attention projection modules из
   закреплённого `state_dict`, не выводить их из mutable library class.
5. **[VERIFIED FACT]** Записать tokenizer/chat-template hashes без изменения
   tokenizer.

**[VERIFIED FACT]** Placeholders `sha256:...`, `artifact://...` и
`run://NOT_RUN/...` заменяются registry. Стадия остаётся `planned`, пока inputs
не закреплены, и не получает release status без machine-readable evidence всех
gates.

## Инварианты precision и execution

- **[VERIFIED FACT]** BF16 — master и единственная разрешённая merge precision.
- **[VERIFIED FACT]** Merge поверх FP8, INT8, INT4 и иных quantized weights запрещён.
- **[VERIFIED FACT]** Каждый source adapter сохраняется после merge.
- **[RISK]** Multi-node H200 topology считается допустимой только после provider
  attestation NVLink/NVSwitch внутри узла и InfiniBand между узлами; наличие
  конкретного allocation не заявляется.
- **[VERIFIED FACT]** Локальное выполнение весов, training, fine-tuning, merge и
  inference запрещено.
- **[EXPERIMENT REQUIRED]** FP8 создаётся только от gate-passing immutable BF16
  `M4` и обязан пройти parity против этого parent.

## Context policy

**[ENGINEERING HYPOTHESIS]** Первый training/evaluation envelope — 32 768
tokens. Расширение до 65 536 — отдельный gate. **[EXPERIMENT REQUIRED]** Native
262 144-token window остаётся evaluation-only до прохождения long-context
quality, safety, memory и latency gates.
