---
name: discover-research-idea
description: Enter dsh_autoresearch from a broad research direction that lacks one established runnable method. Use when the user asks to find or discover an IDEA, explore a broad topic, build a research direction from literature, or autonomously carry a direction through experiments and optionally a paper.
---

# Discover a Research Idea

Turn a broad direction into one bounded, literature-grounded, experimentally testable idea, then enter the common performance pipeline. Avoid a large brainstorm followed by parallel pilots.

## Freeze the problem before generating ideas

Read the direct human objective, project instructions, any code or datasets, local papers, bibliography, notes, prior failures, compute constraints, and non-goals. Write `research/PROBLEM_ANCHOR.md` from the preset template with one problem, one primary metric, one fixed evaluation setting, a protected-data rule, and a compute bound.

Persist:

- `entry_mode=broad-direction`;
- `deliverable=paper` only when the original human objective explicitly includes a manuscript, PDF, or complete research-to-paper lifecycle; otherwise use `method`;
- the named target venue, or no venue for a venue-neutral paper.

If the direction cannot be made falsifiable without changing the user's objective, metric, protected data, or material budget, ask only for that decision. Do not ask the user to choose among ordinary candidate mechanisms.

## Establish a comparable starting point

Identify the strongest runnable reference implementation or the smallest faithful benchmark harness that exposes the anchored problem. Prefer maintained official code already present in the workspace. Do not invent a new method before measuring this reference.

Load `baseline-assessment` and establish a reproducible baseline result under the anchored protocol. If no faithful runnable baseline can be obtained within the budget, report the concrete missing dependency; do not manufacture an IDEA ranking without an evaluation anchor.

Initialize the common state after baseline evidence exists:

```bash
python3 <preset>/tools/transition_guard.py init <root> \
  --entry-mode broad-direction --deliverable <method|paper> \
  --objective "<anchored objective>" --primary-metric "<metric>" \
  --metric-direction <higher|lower> --target-delta "<minimum gain>" \
  --baseline-run "<run id>" --baseline-artifact "<raw result path>"
```

Add `--target-venue "<venue>"` only when the human named one.

## Discover one idea through the common loop

Load `depth-research-loop`. Its literature phase deep-reads the nearest mechanisms and its mapping phase allocates three stable candidate IDs by default. Rank candidates by match to the measured failure, source evidence, distinct project contribution, falsifiability, and screening cost. Implement and train only one candidate at a time.

Require a targeted closest-work check before selecting a candidate. Record eliminated ideas and negative pilots concisely. When a candidate fails, use the measured failure to select an unused mapped candidate or refresh the literature; do not restart a broad brainstorm, defend the failed thesis, or combine unrelated rescue modules.

Use `create_goal` only for an explicit autonomous or full-lifecycle request. If the persisted deliverable is `paper`, `frozen` is an evidence handoff rather than goal completion: follow the guard's `next_action` into `paper-writing`, using venue-neutral output when no venue was named.
