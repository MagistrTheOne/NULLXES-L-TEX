# Phase 4 — SFT, preference and executable GRPO

## Lineage

`LC256K → SFT → PREF → GRPO`

Every stage emits a complete BF16 parent with fresh optimizer/scheduler state.
There is no adapter/merge lane.

## Objectives

- SFT teaches LÆTEX instruction, coding, tool, evidence, escalation and
  governance contracts using verified examples and protected pretrain replay.
- PREF selects DPO or IPO on an identical controlled dataset/compute comparison;
  reference log-probabilities are hash-bound to the immutable SFT parent.
- GRPO optimizes executable outcomes in isolated sandboxes. Tests, policy checks
  and observed deltas are reward authority; a model judge alone cannot certify
  completion.

## H200 and gates

Planning envelope is 512 minimum / 1024 recommended. Default 8K/32K layout is
512=`TP8×PP8×EP8×CP1×DP1`, 1024=`TP8×PP8×EP16×CP1×DP1`; longer batches use the
approved context profile. Rollout and update rank allocations are separately
recorded and sum to world size.

Promotion requires VETCR gain with capability/context/safety non-inferiority,
tool/evidence validity, no unapproved destructive effect and full lineage. GRPO
requires positive lower confidence bound, reward-hacking findings zero and a
cost per incremental verified completion better than additional SFT.
**[RISK]** Sandbox throughput can dominate H200 utilization; scale-out cannot
hide an orchestration bottleneck.
