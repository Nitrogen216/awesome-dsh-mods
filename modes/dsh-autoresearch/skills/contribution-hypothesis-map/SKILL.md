---
name: contribution-hypothesis-map
description: Convert deep-read literature and the measured baseline failure into a ranked pool of testable adaptation candidates. Use in the mapping phase, after a literature refresh, or after a failed screen when unused mapped candidates remain.
---

# Contribution and Hypothesis Mapping

Map prior contributions to this project's failure before selecting code changes.

## Build the map

Read `research/BASELINE.md`, `research/LITERATURE.md`, prior results, and `research/REJECTED.md`; also read `research/PROBLEM_ANCHOR.md` for a broad-direction entrance. Create three candidates by default and at most five. Before writing rows, run `transition_guard.py allocate-candidates <root> --count <n>` and use exactly the returned ids. For each candidate, write one row in `research/CONTRIBUTION_MAP.md` with:

| Field | Required content |
|---|---|
| candidate id | Guard-allocated stable id |
| source contribution | Paper and the mechanism being reused |
| source assumption | Condition required by the paper |
| baseline match | Evidence that the current failure satisfies or violates that condition |
| exposed problem | Concrete current limitation the candidate addresses |
| insufficient default | Why the inherited or obvious response does not solve it |
| derived requirement | Property an adequate adaptation must satisfy |
| hypothesis | Predicted primary-metric change and mechanism observable |
| falsification | Outcome that rejects the proposed mechanism rather than merely missing a target |
| minimal adaptation | One insertion, replacement, or integration in the current method |
| project contribution | What is modified beyond copying the source method |
| novelty risk | Closest prior combination and remaining distinction |
| screen | Cheapest faithful training comparison and pass threshold |
| cost and risk | Expected compute and likely confounders |

Allow multiple source papers in one candidate only when they support the same mechanism and one attributable implementation. Split independent mechanisms into separate candidates. For a broad direction, reject a candidate whose distinction from the closest prior combination cannot be stated as a falsifiable change.

## Rank and select

Rank by:

1. match between the paper's mechanism and the observed failure;
2. strength of source evidence;
3. expected primary-metric effect under the fixed protocol;
4. distinct project contribution;
5. screening cost and implementation risk.

Do not rank by convenience alone. Reject pure threshold searches, post-hoc score combinations, fallback chains, or a bundle whose parts cannot be attributed.

Before selection, load `askgpt-governor` only when two or more distinct, literature-supported mechanism families remain scientifically defensible, the available evidence cannot distinguish them, and the choice changes the central hypothesis or method architecture. Do not escalate a routine ranking tie, an ordinary unused-candidate choice, or a desire for a second opinion.

Select one unused candidate and state why the observed problem, failed default, and derived requirement make this adaptation the next attributable test. Record why the nearest alternative is not selected; do not hide eliminated ideas. Advance `mapping -> adaptation` with outcome `candidate_selected` and `--candidate-id <guard-allocated-id>`. If no candidate has a defensible mechanism mapping, return `mapping -> literature` with outcome `evidence_gap` and a targeted search question.
