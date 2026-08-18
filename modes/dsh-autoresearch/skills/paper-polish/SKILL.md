---
name: paper-polish
description: Revise a compiled research manuscript through at most two bounded, issue-driven passes and one final factual check. Use after paper compilation to improve claim clarity, literature positioning, structure, terminology, captions, page fit, and layout without numeric reviewer ratings, new experiments, or unsupported content.
---

# Paper Polish

Improve the current manuscript without turning review into an open-ended loop.

Read `../../references/paper-forward-logic.md` and use it as the structural standard for both passes.

## Use two passes at most

### Pass 1: argument and evidence

Check the one-sentence contribution, claim-evidence alignment, scope qualifiers, closest-work positioning, method-to-source distinction, and section order. Reject retrospective rationale: every design choice must follow its exposed problem, insufficient default, and derived requirement. Confirm that each paragraph advances one inference and each figure or theorem advances a claim.

### Pass 2: presentation

Check terminology, notation, paragraph fragmentation, sentence directness, empty professional-sounding terms, captions, table readability, page budget, float placement, and rendered layout. Confirm that field consensus is brief and explanation is concentrated on missing or wrong priors. For each figure, verify its one-sentence takeaway, three-second readability, visual hierarchy, and removal of non-supporting boxes, arrows, panels, or labels.

Represent each actionable issue with severity, location, evidence, and minimal fix. Use critical, major, or minor severity.

Apply critical and major fixes that are supported by existing sources. Apply minor fixes only when local and low risk. Recompile after material edits.

A fresh reviewer may identify issues from the current source and PDF when available, but it is optional. Give the reviewer no prior fix narrative, request location-specific issues rather than a numeric rating, and independently verify every proposed change before applying it.

Stop early when no new material issue remains. If the same concern returns without new evidence, record it once and stop; do not keep rewriting to satisfy wording preferences.

## Run one final factual check

Write paper/FINAL_CHECK.md after the last compile:

1. map every headline claim to its evidence and scope;
2. compare every reported result number with its raw artifact;
3. verify every cited work exists and supports the attached statement;
4. for theory papers only, check assumptions, statements, proof dependencies, and main or appendix consistency;
5. confirm the compiled PDF, figures, tables, and limitations, plus verified page and anonymity rules for a named venue or explicit not-applicable status for `venue-neutral`;
6. list unresolved evidence gaps and the claims they constrain.
7. confirm forward design order, inferential paragraphs, and one-takeaway figures against the shared standard.

This is one consolidated check, not a family of audit artifacts.

Do not add a new experiment, method component, theorem, result, or citation merely because a reviewer asks for it. Record such a request in paper/OPEN_EVIDENCE_GAPS.md and return it to the user. Never alter the promoted research method or research pipeline state from this skill.
