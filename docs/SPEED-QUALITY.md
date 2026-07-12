# Speed / cost / quality strategy

## Статус

- **[VERIFIED FACT]** В этом документе нет benchmark results. Все числовые latency targets ниже — целевые инженерные гипотезы до воспроизводимого H200-прогона.
- **[EXPERIMENT REQUIRED]** Любая runtime-конфигурация проходит один frozen LÆTEX-Bench workload, одинаковые tool budgets и cost accounting.
- **[RISK]** Улучшение tokens/s, TTFT или raw inference cost не считается выигрышем, если падает Verified Enterprise Task Completion Rate либо растёт time/cost per verified task.

## Serving bakeoff

- **[EXPERIMENT REQUIRED]** SGLang и vLLM сравниваются на H200 по warm/cold TTFT, decode throughput, p50/p95 end-to-end latency, long-context stability, tool-call validity, cache isolation, VETCR и cost per verified task.
- **[VERIFIED FACT]** Выбор serving engine не фиксируется по vendor claim или microbenchmark; promotion требует одинаковые checkpoint, precision, prompts, concurrency и verifier workload.
- **[ENGINEERING HYPOTHESIS]** BF16 является reference runtime. FP8 принимается только после parity по VETCR, tool/identity/policy gates и измеримого выигрыша throughput/cost.
- **[VERIFIED FACT]** MXFP4 отклонён для E-01 на H200: он не является базовым H200 execution target и добавляет отдельный kernel/quality risk без принятой необходимости.

## Runtime optimizations

- **[ENGINEERING HYPOTHESIS]** Prefix cache и repository-state cache уменьшают повторную prefill-работу.
- **[VERIFIED FACT]** Cache keys включают tenant, repository snapshot, policy digest, permissions, template/runtime revision и sensitivity class; cross-tenant cache reuse запрещён.
- **[RISK]** Shared cache без tenant namespace является каналом утечки и блокирует release.
- **[EXPERIMENT REQUIRED]** Continuous batching принимается только после проверки fairness, tail latency, deadline isolation и отсутствия cross-request state mixing.
- **[EXPERIMENT REQUIRED]** Speculative decoding включается только после acceptance experiment с малой draft-моделью LÆTEX: exact output contract, VETCR/non-inferiority, tool validity и реальный end-to-end speedup.
- **[ENGINEERING HYPOTHESIS]** Structured retrieval минимизирует prompt stuffing: модель получает task-relevant slices, version IDs, provenance и policy decisions, а полный CodeWorld остаётся в authoritative stores.
- **[ENGINEERING HYPOTHESIS]** Независимые build/test/security/policy verifiers исполняются параллельно, если их side effects отсутствуют и dependency graph это разрешает.
- **[RISK]** Verification parallelism запрещён для зависимых или изменяющих состояние checks; ложный параллелизм создаёт stale-state verdict.

## Экономика

- **[VERIFIED FACT]** Cost per verified task включает H200 inference, sandbox/tools, storage/network, retries, verification и измеренный human-review labor; failed tasks остаются в знаменателе workload cost.
- **[EXPERIMENT REQUIRED]** Candidate сравнивается с baseline на одном task mix, price timestamp, timeout/retry policy и labor rate card.
- **[RISK]** Снижение cost/token не доказывает снижение cost per verified task.

## Latency targets

| Workflow | Target p50 | Target p95 | Статус |
|---|---:|---:|---|
| Warm interactive TTFT | `<=0.7 s` | `<=1.5 s` | **[ENGINEERING HYPOTHESIS]** Target, не результат |
| Architecture plan | `20–45 s` | `<=90 s` | **[ENGINEERING HYPOTHESIS]** Target, не результат |
| Small verified patch | `2–5 min` | `<=10 min` | **[ENGINEERING HYPOTHESIS]** Target, не результат |
| Verified PR-level task | `15–45 min` | `<=90 min` | **[ENGINEERING HYPOTHESIS]** Target, не результат; human wait исключён |

- **[EXPERIMENT REQUIRED]** Отчёт отдельно публикует queue, prefill, decode, tool, sandbox, verifier и retry time, а также cold/warm и cache-hit/miss strata.
- **[RISK]** Human approval wait исключается только из model-system latency и публикуется отдельно; скрывать его из полного business lead time запрещено.
