---
name: improve-existing-project
description: Enter the dsh_autoresearch pipeline from an existing runnable project or method. Use when the user asks to improve, optimize, train, continue, or autonomously research a codebase that already has an implementation and evaluation path; preserve whether the original human objective ends at a promoted method or also requires a paper.
---

# Improve an Existing Project

Own the entry decision and hand the scientific work to `depth-research-loop`. Do not replace its phase skills.

## Confirm this is the existing-project entrance

Use this entrance when the workspace already contains a runnable method and an evaluation path, even if its current result is weak. If only a broad direction exists and no comparable implementation can be identified, load `discover-research-idea` instead. Inspection, diagnosis, comparison, and status requests remain read-only.

Read the current direct human objective before creating research state. Persist:

- `entry_mode=existing-project`;
- `deliverable=paper` only when that objective explicitly asks for a paper, manuscript, PDF, or the complete research-to-paper lifecycle; otherwise use `method`;
- `target_venue` only when the human names one. A paper deliverable without a venue is valid and means `venue-neutral`.

Do not infer a paper deliverable from an existing `.tex` file, a paper mentioned in project notes, or a downstream suggestion.

## Establish the common pipeline

1. Inspect project instructions, implementation, evaluation code, configs, splits, prior results, and local literature.
2. Load `baseline-assessment`. Reuse comparable baseline evidence or run the official baseline when it is absent.
3. Initialize the canonical state only after the baseline artifact exists:

```bash
python3 <preset>/tools/transition_guard.py init <root> \
  --entry-mode existing-project --deliverable <method|paper> \
  --objective "<objective>" --primary-metric "<metric>" \
  --metric-direction <higher|lower> --target-delta "<minimum gain>" \
  --baseline-run "<run id>" --baseline-artifact "<raw result path>"
```

Add `--target-venue "<venue>"` only when the human named one.

4. Load `depth-research-loop` and follow the phase returned by the guard.

Use `create_goal` only when the direct human request is explicitly autonomous or asks for the full lifecycle. Preserve the original completion boundary in the goal objective. A method-only goal may complete at `frozen`; a paper goal may not complete until `paper/main.pdf` and `paper/FINAL_CHECK.md` exist.

## Preserve the requested handoff

Every continuation begins by showing `research/STATE.json` through the guard. When its `next_action` names `paper-writing`, load that skill immediately and pass the persisted target venue. Do not ask for a venue when it is absent; use its venue-neutral path. Do not create a second goal for the paper phase.

Never change `entry_mode`, `deliverable`, or `target_venue` because an experiment succeeds or fails. A later direct human request may start paper writing explicitly, but ordinary research output cannot widen the original deliverable.
