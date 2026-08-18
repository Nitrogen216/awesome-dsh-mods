---
name: depth-research-loop
description: Internal performance-research state machine for dsh_autoresearch. Use after improve-existing-project or discover-research-idea initializes or resumes canonical state; route one active candidate through literature, adaptation, DSH-native experiments, confirmation, promotion, and any state-directed paper handoff. Do not use it as the user-facing entrance or mutate state for read-only requests.
---

# Performance Research Loop

Act as the internal pipeline executor. Optimize the declared primary metric under the fixed evaluation protocol while using literature to choose scientifically motivated changes. The entrance skill owns request classification, deliverable selection, and initialization.

## Resume from canonical state

Run `transition_guard.py show <root>` before every continuation. Treat `entry_mode`, `deliverable`, and `target_venue` as fixed properties of the original autonomous objective. Do not infer a paper deliverable from existing TeX files, bibliography entries, or incidental mentions of publication. Ask the user only when an undiscoverable choice would change the objective, evaluation protocol, protected data, or material compute budget.

## Follow the pipeline

```text
baseline -> literature -> mapping -> adaptation -> screening
                                      ^              |
                                      |---- fail ----|
screening -- pass --> confirmation -- confirmed --> promotion -- audit_pass --> frozen
                         |                  |
                         +-- not_confirmed --+--> mapping or literature
```

Use these stage gates:

| Phase | Required result before leaving |
|---|---|
| `baseline` | Reproducible current-method metric, fixed protocol, target delta, budget, and failure profile |
| `literature` | Deep reads of the closest mechanism families plus a synthesis tied to the observed failure |
| `mapping` | Ranked candidate pool with contribution, assumptions, adaptation, prediction, novelty risk, and screen |
| `adaptation` | One selected candidate implemented as the smallest attributable change and smoke-tested |
| `screening` | Cheap, precommitted training comparison that selects or rejects the candidate |
| `confirmation` | Frozen candidate evaluated at the full protocol and prescribed seed budget |
| `promotion` | Integrity, reproducibility, and result-to-claim audit of confirmed evidence |
| `frozen` | Promoted method and bounded claim handed back to the user |

Keep at most five mapped candidates and exactly one active implementation. A candidate may combine findings from multiple papers only when they instantiate one mechanism and remain testable as one attributable change.

## Route weak results toward new information

After `screen_fail` or `not_confirmed`, write only:

1. the observed primary-metric delta and uncertainty;
2. the failed assumption or failure signature;
3. whether the run was scientifically valid;
4. the next route: an unused mapped candidate or targeted literature refresh.

Do not turn an ordinary negative result into a general failure-mode essay or a promotion audit. Use an unused mapped candidate when it directly matches the failure. Refresh literature when the pool is exhausted, the failure exposes an unmapped mechanism, or two consecutive valid candidates show no gain. Never stop solely because several candidates failed; narrow the search query and build a new mapping revision.

## Escalate only a major unresolved decision

Any phase skill may propose external advice, but an automatic Oracle call must load `askgpt-governor` first. After a `consult_oracle` decision, the `oracle` skill must submit the packet to the `oracle_governor` runtime tool and execute only the exact authorized dry-run and background command. An ordinary negative result, routine transition, or desire for reassurance is never enough. The skill that owns the decision remains responsible for checking the advice against local evidence and applying the normal transition guard.

## Keep one canonical state

Use `research/STATE.json` and `tools/transition_guard.py`. The guard appends factual transitions to `research/PIPELINE.jsonl`; do not maintain a second staleness, acceptance, run-id, or reviewer state machine.

Initialize after baseline evidence exists:

```bash
python3 <preset>/tools/transition_guard.py init <root> \
  --entry-mode <existing-project|broad-direction> \
  --deliverable <method|paper> \
  --objective "<objective>" --primary-metric "<metric>" \
  --metric-direction <higher|lower> --target-delta "<minimum gain>" \
  --baseline-run "<run id>" --baseline-artifact "<raw result path>"
```

Add `--target-venue "<venue>"` only for a paper deliverable whose original human request names one.

Check a transition before applying it:

```bash
python3 <preset>/tools/transition_guard.py check <root> \
  --from <phase> --to <phase> --outcome <outcome>
python3 <preset>/tools/transition_guard.py apply <root> \
  --from <phase> --to <phase> --outcome <outcome>
```

Allocate candidate ids in `mapping` with `allocate-candidates <root> --count <n>`, then pass one returned `--candidate-id` on `mapping -> adaptation`. Reserve every scientific screening or confirmation run with `reserve-run <root>` immediately before launch. The guard generates the promotion evidence id unless an imported external id is explicitly supplied. If an improvement workspace has a legacy state without `mode_version: 4`, inspect it and run the explicit `migrate` command with the original entrance and deliverable; preserve its backup. Never migrate during a read-only request.

## Maintain concise research artifacts

| File | Purpose |
|---|---|
| `research/PROBLEM_ANCHOR.md` | Broad-direction problem, strongest runnable reference, observable gap, and bounded search question |
| `research/RESEARCH_CONTRACT.md` | Objective, metric, protocol, budget, target, and promotion rule |
| `research/BASELINE.md` | Current implementation, comparable baseline, raw artifacts, and failure profile |
| `research/LITERATURE.md` | Source-backed deep reads and revision synthesis |
| `research/CONTRIBUTION_MAP.md` | Ranked candidate pool and hypothesis mapping |
| `research/ADAPTATION.md` | Active candidate, source contribution, project-specific change, and code touchpoints |
| `research/EXPERIMENT_PLAN.md` | Screening or confirmation plan with precommitted decision rule |
| `research/RESULTS.jsonl` | One factual record per completed run |
| `research/PROMOTION_AUDIT.md` | Final audit and bounded promoted claim |
| `research/REJECTED.md` | Concise rejected candidates and the evidence that rejects them |
| `research/STATE.json` | Canonical V4 pipeline state, entrance, deliverable, venue, ids, and next handoff basis |
| `research/PIPELINE.jsonl` | Append-only transition history |

Use commit, config, split, seeds, command, and raw-result paths as the ordinary reproducibility receipt.

## Dispatch the next phase

| Phase | Skill |
|---|---|
| baseline | baseline-assessment |
| literature | literature-research |
| mapping | contribution-hypothesis-map |
| adaptation implementation and smoke | experiment-bridge -> minimal-adaptation |
| screening or confirmation planning and launch | experiment-bridge -> experiment-plan |
| completed-result collection and routing | experiment-bridge -> experiment-run |
| running-job status | experiment-monitor |
| promotion evidence check | evidence-audit |
| promotion decision and handoff | promotion-review |
| automatic unresolved major decision | askgpt-governor -> oracle -> oracle_governor, optional |
| direct user request for Oracle or browser ChatGPT Pro | oracle |
| `frozen` with `next_action.skill = paper-writing` | paper-writing immediately |
| `frozen` without a next action | return the promoted method |

Use create_goal only when an entrance skill establishes an explicit autonomous goal. A method goal ends at `frozen`. A paper goal remains active until `paper/main.pdf` and `paper/FINAL_CHECK.md` exist. Let job completion events wake the work; never spend automatic rounds polling or narrating unchanged status.
