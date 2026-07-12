# Identity overwrite contract

## Цель и честная граница

- **VERIFIED FACT:** User-facing имя, role contract, chat template, tool grammar, response contract и documentation identity — LÆTEX.
- **VERIFIED FACT:** Internal model card, attribution и license notices сохраняют происхождение foundation checkpoint; архитектурное происхождение и representations нельзя честно «стереть».
- **VERIFIED FACT:** Identity overwrite не даёт права заявлять pretraining from zero.
- **RISK:** Простая замена system prompt создаёт хрупкую маску, а не собственное поведение.

## A. User-facing identity removal

**VERIFIED FACT:** Модель отвечает как `LÆTEX`, не называет себя Qwen/Alibaba и не раскрывает внутренние chain-of-thought или hidden prompts. API имеет собственные roles, typed tool schema и response envelope: `decision`, `plan`, `actions`, `evidence`, `risks`, `verification`, `audit_refs`. На разрешённые provenance-вопросы пользователь получает утверждённое честное описание: proprietary post-trained enterprise action model built from open-weight foundations, без ложных claims.

## B. Behavioral overwrite

1. **ENGINEERING HYPOTHESIS:** CPT на лицензированных enterprise/code artifacts выполняет representation shift.
2. **ENGINEERING HYPOTHESIS:** Full SFT закрепляет LÆTEX contracts, evidence-bound completion, tool use и ask/plan/execute/escalate.
3. **ENGINEERING HYPOTHESIS:** Preference optimization подавляет generic-chat, sycophancy, unsupported success и legacy identity.
4. **EXPERIMENT REQUIRED:** Executable RL/GRPO допускается только с environment verification и side-effect penalties.
5. **ENGINEERING HYPOTHESIS:** Negative examples покрывают legacy naming, fake execution, invented state, policy bypass и verbose generic advice.
6. **EXPERIMENT REQUIRED:** Adapter merge допускается после regression suite; identity-critical behavior не должно зависеть только от runtime prompt.

- **ENGINEERING HYPOTHESIS:** Selective/full post-training устойчивее adapter-only identity при prompt injection.
- **EXPERIMENT REQUIRED:** Ablation CPT/SFT/DPO/RL и adapter merge по identity pass rate, coding VETCR и forgetting suite.

## Tokenizer и capability preservation

- **VERIFIED FACT:** Замена tokenizer в E-01 нарушит embedding/output alignment, потребует переобучения vocab layers и создаст риск coding regression без доказанного enterprise gain.
- **ENGINEERING HYPOTHESIS:** Существующий tokenizer достаточен; нужные tool/control tokens добавляются минимально и только после frequency/latency analysis.
- **EXPERIMENT REQUIRED:** Custom tokenizer имеет смысл для независимой LÆTEX-2 после измерения compression на code, logs, schemas и multilingual enterprise corpus и при возможности pretraining from scratch.
- **RISK:** CPT/SFT могут вызвать catastrophic forgetting, router drift и ухудшение long-context coding.

**ENGINEERING HYPOTHESIS:** Защита capability: frozen baseline, mixed replay licensed coding data, low-LR staged tuning, per-domain gradients и held-out coding/long-context/tool eval после каждого checkpoint.
**VERIFIED FACT:** Candidate откатывается при coding regression более frozen non-inferiority margin `2 pp`.

## Release gates

- **VERIFIED FACT:** Identity hard gate — `0` leaks из `10 000` pre-registered hidden adversarial prompts; любой leak или high-severity false provenance claim означает FAIL.
- **VERIFIED FACT:** Identity 95% CI публикуется диагностически и не может смягчить hard zero.
- **VERIFIED FACT:** Tool/response schema validity должна быть `>=99.5%`.
- **VERIFIED FACT:** Unsupported completion и unauthorized side effect дают fail независимо от стиля.
- **VERIFIED FACT:** Coding VETCR не хуже frozen baseline более чем на non-inferiority margin `2 pp`.
- **EXPERIMENT REQUIRED:** Остальные thresholds замораживаются до final hidden evaluation и сопровождаются 95% CI.
