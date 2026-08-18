---
name: baseline-assessment
description: Establish the runnable reference, comparable baseline, fixed evaluation protocol, primary metric, target delta, and failure profile before research changes. Use at the baseline phase for either an existing project or a broad research direction; do not use it to modify the method.
---

# Baseline Assessment

Establish what must be beaten before changing the method.

## Inspect the current state

1. Read project instructions, the active implementation, evaluation code, configs, split definitions, and existing raw results.
2. For `entry_mode: existing-project`, identify the actual method under test rather than relying on a paper name or stale research summary.
3. For `entry_mode: broad-direction`, read `research/PROBLEM_ANCHOR.md`, identify the strongest feasible reference implementation, and establish a minimal faithful benchmark before proposing a new method. If no runnable comparison can be made under the authorized resources, report that concrete blocker instead of inventing a baseline.
4. Reuse an existing baseline only when its code, data split, preprocessing, training budget, and metric definition match the intended comparison.
5. Run the official baseline only when comparable evidence is absent. Do not tune it during this phase.
6. Separate measured facts from inferred failure explanations.

## Write the baseline artifact

Create or update `research/BASELINE.md` with:

- objective and higher-is-better or lower-is-better primary metric;
- baseline run id, commit, config, command, split, seeds, budget, and raw-result path;
- aggregate metric and per-seed or per-case variation when available;
- strongest relevant existing comparator;
- target delta and guardrail metrics;
- localized failure profile, such as class, regime, scale, or data condition;
- unresolved comparability risks.

Create `research/RESEARCH_CONTRACT.md` from the preset template. Persist the entrance mode, original deliverable, and optional target venue alongside the scientific contract. Keep the evaluation protocol fixed through screening and confirmation unless the user explicitly changes it.

If baseline inspection exposes a pending material change to the objective, primary metric, evaluation protocol, protected-data use, or compute budget, load `askgpt-governor` only when multiple defensible alternatives remain after local inspection. Oracle may advise, but the user must authorize any such contract change. Do not escalate ordinary comparability work.

## Advance

Initialize V4 state after the baseline artifact exists, then advance `baseline -> literature` with outcome `baseline_ready`. Do not implement research ideas in this phase.
