# ADR-0001: сохранить upstream tokenizer в derivative E-01

- **VERIFIED FACT:** Статус: Superseded by ADR-0008.
- **VERIFIED FACT:** Область: архивное решение для superseded Qwen-derivative E-01.
- **VERIFIED FACT:** Дата supersession: 2026-07-13.

## Контекст

- **VERIFIED FACT:** `Qwen/Qwen3-Coder-480B-A35B-Instruct` config фиксирует vocabulary size 151 936 и BF16 embedding/output weights.
- **VERIFIED FACT:** E-01 использует этот post-trained Instruct checkpoint напрямую; 80B Base не входит в lineage.
- **RISK:** Замена vocabulary/token IDs инвалидирует совместимость embeddings, output head, chat/tool tokenization и часть learned code representations.
- **ENGINEERING HYPOTHESIS:** Выигрыш custom enterprise tokens в E-01 меньше стоимости retokenization, embedding adaptation и regression risk.

## Решение

- **VERIFIED FACT:** E-01 сохраняет upstream tokenizer, vocabulary и token IDs.
- **ENGINEERING HYPOTHESIS:** Собственный LÆTEX chat template, tool grammar и response contract реализуются поверх существующего tokenizer.
- **VERIFIED FACT:** Tokenizer hash входит в каждый checkpoint/runtime manifest.
- **VERIFIED FACT:** Один tokenizer hash наследуется через `S0/M1/M2/M3/M4`; silent mutation между train, verify и BF16 merge запрещена.

## Последствия

- **VERIFIED FACT:** Сохраняется checkpoint compatibility и уменьшается число изменяемых компонентов.
- **RISK:** Некоторые enterprise identifiers и schemas токенизируются неидеально; это измеряется tokens-per-artifact и latency, а не исправляется ad hoc vocabulary patch.
- **EXPERIMENT REQUIRED:** Identity overwrite оценивается adversarially; смена tokenizer не считается механизмом удаления identity.

## Условия пересмотра

- **EXPERIMENT REQUIRED:** Custom tokenizer допустим для независимого LÆTEX-2 до pretraining, если corpus study показывает устойчивый compression/quality gain и migration cost отсутствует.
- **RISK:** Добавление tokens после E-01 release требует нового model lineage и полного regression cycle; silent tokenizer mutation запрещена.

## Supersession

- **VERIFIED FACT:** ADR-0008 заменяет это решение, потому что принятый ADR-0007 определяет E-01 как independent from-scratch model без upstream tokenizer.
- **VERIFIED FACT:** Содержимое выше сохраняется как историческая запись и не определяет canonical tokenizer E-01.
