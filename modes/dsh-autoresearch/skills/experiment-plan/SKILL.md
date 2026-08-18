---
name: experiment-plan
description: Plan either a cheap small-scale training screen or a full-budget confirmation for the active candidate. Use in the screening or confirmation phase before launching training; keep the metric, controls, budget, and decision rule fixed in advance.
---

# Experiment Plan

Plan the experiment appropriate to the current phase as a component of `experiment-bridge`. Every block must say which claim it tests, why the comparison exists, what success means, what a valid failure means, and which raw artifact, table, or figure it will produce. Write the plan to `research/EXPERIMENT_PLAN.md` before launch.

## Plan a screening run

Use the smallest training setup that preserves the mechanism under test:

- compare the active candidate with the frozen comparable baseline;
- change only the mapped adaptation;
- use a representative subset, shortened schedule, and one or two predetermined seeds when faithful;
- keep preprocessing, split semantics, metric implementation, and evaluation code unchanged;
- precommit the primary-metric pass threshold, guardrails, and invalid-run conditions;
- include one mechanism observable only when it distinguishes the hypothesis;
- specify how screening fidelity will be checked.
- state the valid-failure route: reject the mechanism, revise one assumption, use an unused mapped candidate, or refresh literature around the observed signature.

A screen selects candidates; it does not support a final performance claim.

## Plan a confirmation run

Use confirmation only after `screen_pass`:

- freeze the candidate code and hyperparameters selected before confirmation;
- use the full training schedule, full evaluation protocol, and project-prescribed seeds;
- use at least three predetermined seeds when the project has no seed rule;
- compare against the exact baseline and all required strong comparators;
- precommit aggregation, uncertainty, statistical test when appropriate, and promotion threshold;
- forbid candidate changes after observing confirmation results; a changed candidate must be screened again.

Separate must-run comparisons required for the central claim from useful follow-ups. A follow-up cannot become a promotion prerequisite after results are seen. Assign every planned comparison to a claim id and every output table or figure to its authoritative raw path.

Before committing confirmation, load `askgpt-governor` only when an unresolved choice materially changes the evaluation obligations or compute commitment and cannot be settled from the research contract, literature, screening evidence, or project rules. Do not escalate ordinary seed counts, runtime estimates, thresholds, or any choice already fixed by the protocol. Oracle cannot authorize a budget or protocol change for the user.

## Protect validity

Keep test or held-out labels out of candidate selection. Do not change the evaluation protocol to rescue a candidate. Avoid a grid search disguised as one experiment. Record the selected DSH-accessible backend, expected runtime, device, launch command, config, output paths, recovery procedure, and the distinction between the scientific run id and the DSH background job id. `experiment-bridge` reserves the run id immediately before launch.
