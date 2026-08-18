---
name: askgpt-governor
description: Gate and submit an automatic Oracle/ChatGPT Pro consultation for one unresolved major scientific decision. Use only when a phase skill faces two or three defensible alternatives that local evidence and primary literature cannot resolve and the choice materially changes the objective or protocol, central mechanism, expensive confirmation, promotion claim, or central manuscript framing; return continue_local for routine research, implementation, negative results, monitoring, and writing polish.
---

# Major-Decision Oracle Governor

Act as the sole reasoning gate for automatic Oracle calls from other dsh_autoresearch skills. The `oracle_governor` tool is the runtime enforcement point. Do not call Oracle merely because external advice might be useful.

## Decide eligibility first

Return `consult_oracle` only when all five conditions hold:

1. One concrete decision is pending now.
2. Two or three scientifically defensible alternatives remain.
3. The choice materially changes the research direction, evaluation obligations, compute commitment, promotion claim, or central paper contribution.
4. The baseline, primary literature, local code, and available results have been inspected and cannot resolve the alternatives.
5. A reasoned recommendation can change the immediate next action.

Qualifying decisions are limited to:

- changing the user objective, primary metric, evaluation protocol, protected-data use, or material compute budget;
- choosing between distinct literature-supported mechanism families when that choice determines the central hypothesis or method architecture;
- committing materially expensive confirmation or responding to a protocol-level contradiction that changes the remaining program;
- promoting, freezing, or rejecting the method when the same valid evidence supports materially different bounded claims;
- choosing between scientifically different central manuscript framings that change the scope of the claimed contribution.

If any condition fails, return `continue_local` without loading Oracle, creating an advisor artifact, or reporting a missing-review limitation. A direct user request for Oracle bypasses this automatic eligibility gate but not the safety and evidence rules in `oracle`.

When qualification is ambiguous, return `continue_local`. Do not broaden “material” beyond the enumerated decisions.

## Reject routine escalation

Return `continue_local` for:

- ordinary screen failure, confirmation failure, or failure-mode explanation;
- routine candidate ranking when the contribution map already distinguishes the options;
- implementation design, debugging, tests, hyperparameters, thresholds, or small budget choices within the fixed contract;
- job monitoring, literature search or summarization, citation lookup, and deterministic integrity or reproducibility checks;
- ordinary state transitions, formatting, figure styling, compilation, copyediting, and reviewer reassurance;
- a decision already consulted on unless new evidence materially changes its alternatives.

## Consult once

After deciding `consult_oracle`:

1. Assign a short semantic decision id such as `mapping:mechanism-family:v1` or `paper:central-claim:v1`. Search the artifact that owns the choice; if that id already has an Oracle session and no new evidence changes the alternatives, reuse the recorded advice or reattach instead of consulting again.
2. Prepare one bounded packet containing the decision id, exact decision, enumerated material consequence, two or three alternatives, baseline and code evidence, primary-literature evidence, available experiment evidence, unresolved uncertainty, the immediate action under each alternative, and one to eight literal workspace-relative evidence files.
3. Load `oracle`, then call `oracle_governor` with basis `major_decision`. Do not construct a CLI command yourself. If the runtime tool returns `continue_local`, return to the owning skill.
4. Execute only the exact foreground dry-run command returned by the runtime tool. After it succeeds, execute only the exact run command with the shell tool's `run_in_background: true`; track the returned job instead of busy-polling.
5. Never switch to API, a different model, a weaker thinking tier, manual paste, or an altered file set. The runtime guard rejects commands that do not match its authorization.
6. Verify cited papers against primary sources and technical claims against local code, results, and tests.

If Oracle is unavailable, continue with bounded local reasoning or ask the user when the choice is user-owned. Do not edit provider configuration, expose credentials, or block unrelated pipeline work.

Record only the semantic decision id, Oracle session reference, recommendation, and the executor's final local decision in the artifact that already owns the choice, such as `research/CONTRIBUTION_MAP.md`, `research/EXPERIMENT_PLAN.md`, `research/PROMOTION_AUDIT.md`, or `paper/PAPER_PLAN.md`. Do not compute a hash or create a parallel advisor ledger or state machine. Oracle advice cannot authorize user-owned changes or advance pipeline state by itself.
