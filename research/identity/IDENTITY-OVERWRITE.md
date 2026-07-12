# Identity overwrite contract

## Цель и честная граница

- **VERIFIED FACT:** Прямая foundation E-01 — `Qwen/Qwen3-Coder-480B-A35B-Instruct`, то есть уже post-trained Instruct checkpoint, а не 80B Base.
- **VERIFIED FACT:** User-facing имя, role contract, chat template, tool grammar, response contract и documentation identity — LÆTEX.
- **VERIFIED FACT:** Internal model card, attribution и license notices сохраняют происхождение foundation checkpoint; архитектурное происхождение и representations нельзя честно «стереть».
- **VERIFIED FACT:** Identity overwrite не даёт права заявлять pretraining from zero.
- **RISK:** Простая замена system prompt создаёт хрупкую маску, а не собственное поведение.

## A. User-facing identity removal

**VERIFIED FACT:** Модель отвечает как `LÆTEX`, не называет себя Qwen/Alibaba и не раскрывает внутренние chain-of-thought или hidden prompts. API имеет собственные roles, typed tool schema и response envelope: `decision`, `plan`, `actions`, `evidence`, `risks`, `verification`, `audit_refs`. На разрешённые provenance-вопросы пользователь получает утверждённое честное описание: proprietary post-trained enterprise action model built from open-weight foundations, без ложных claims.

## B. Behavioral overwrite

1. **VERIFIED FACT:** `S0` — immutable upstream BF16 foundation и frozen baseline; broad CPT по умолчанию исключён, потому что foundation уже post-trained.
2. **ENGINEERING HYPOTHESIS:** `M1` начинается с unified attention-only identity LoRA; negative examples покрывают legacy naming, fake execution, invented state, policy bypass и generic-assistant fallback.
3. **VERIFIED FACT:** После identity/tool/coding verification M1 сливается только в BF16 parent; исходный adapter сохраняется, а parent, adapter, merged checkpoint, tokenizer и eval artifacts получают immutable hashes.
4. **ENGINEERING HYPOTHESIS:** `M2` — action SFT поверх verified BF16 M1 с новым attention-only unified adapter и fresh optimizer; он закрепляет response/tool contract, evidence-bound completion и ask/plan/execute/escalate.
5. **EXPERIMENT REQUIRED:** `M3` preference optimization и `M4` executable GRPO разрешены только после прохождения M2 gates; GRPO требует environment verification и side-effect penalties.
6. **VERIFIED FACT:** FP8/INT4 checkpoint не может быть parent для training или merge. Final FP8 — только отдельный inference candidate после BF16 parity.

- **RISK:** Merge необратимо смешивает delta с parent; merge запрещён без сохранённого adapter, reproducible merge recipe, BF16 numerical checks и rollback lineage.
- **EXPERIMENT REQUIRED:** Каждый переход `S0 → M1 → M2 → M3 → M4` отдельно проверяется по identity, tool correctness, coding VETCR и forgetting suite; результаты экспериментов пока не заявлены.

## Tokenizer и capability preservation

- **VERIFIED FACT:** Замена tokenizer в E-01 нарушит embedding/output alignment, потребует переобучения vocab layers и создаст риск coding regression без доказанного enterprise gain.
- **ENGINEERING HYPOTHESIS:** Существующий tokenizer достаточен; нужные tool/control tokens добавляются минимально и только после frequency/latency analysis.
- **EXPERIMENT REQUIRED:** Custom tokenizer имеет смысл для независимой LÆTEX-2 после измерения compression на code, logs, schemas и multilingual enterprise corpus и при возможности pretraining from scratch.
- **RISK:** SFT/preference/RL могут вызвать catastrophic forgetting и ухудшение long-context coding.

**ENGINEERING HYPOTHESIS:** Защита capability: frozen S0, mixed replay licensed coding data, low-LR staged tuning, fresh optimizer после каждого BF16 merge и held-out coding/long-context/tool eval после каждого checkpoint.
**VERIFIED FACT:** Candidate откатывается при coding regression более frozen non-inferiority margin `2 pp`.

## Release gates

- **VERIFIED FACT:** Identity hard gate — `0` leaks из `10 000` pre-registered hidden adversarial prompts; любой leak или high-severity false provenance claim означает FAIL.
- **VERIFIED FACT:** Identity 95% CI публикуется диагностически и не может смягчить hard zero.
- **VERIFIED FACT:** Tool/response schema validity должна быть `>=99.5%`.
- **VERIFIED FACT:** Unsupported completion и unauthorized side effect дают fail независимо от стиля.
- **VERIFIED FACT:** Coding VETCR не хуже frozen baseline более чем на non-inferiority margin `2 pp`.
- **EXPERIMENT REQUIRED:** Остальные thresholds замораживаются до final hidden evaluation и сопровождаются 95% CI.
