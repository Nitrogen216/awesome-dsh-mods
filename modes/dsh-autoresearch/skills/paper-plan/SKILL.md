---
name: paper-plan
description: Build a source-grounded paper plan from promoted research evidence and deeply read literature. Use before drafting a new manuscript or restructuring an existing one to define the one-sentence contribution, claims-evidence matrix, related-work positioning, section budget, figures, tables, and verified citation needs.
---

# Paper Plan

Plan the argument before writing prose.

Read `../../references/paper-forward-logic.md` before building or restructuring the plan.

## Read authoritative inputs

Read the promotion audit, raw-result index, literature synthesis, contribution map, adaptation record, and any existing manuscript. Verify the target venue and its current rules from an official source when the venue is known. When the target is `venue-neutral`, use an internal working page budget for coherence but label venue page limits, anonymity, and formatting rules not applicable.

If the evidence is provisional, label it as such. Do not treat screening results or a literature claim as confirmed project evidence.

If the literature synthesis does not cover the closest current work needed for positioning, run a targeted paper search. Deep-read the primary paper, supplement, and official implementation when available; extract its exact contribution, assumptions, controlled evidence, limitation, and relation to the promoted method. Use this search to strengthen positioning and citations, not to silently modify the frozen method.

If two scientifically different central contribution framings remain supported after the evidence and closest literature are read, and choosing between them materially changes the headline claim's scope, load `askgpt-governor` once. Do not escalate wording, section order, citation lookup, figure choice, or routine positioning.

## Build the plan

Write paper/PAPER_PLAN.md with:

1. target venue or `venue-neutral`, paper type, official or working page budget, and one-sentence contribution;
2. a claims-evidence matrix;
3. a contribution-positioning map;
4. a reader-state and causal design chain for every major method choice;
5. a section-by-section argument and page budget;
6. a figure and table plan tied to one-sentence takeaways and raw sources;
7. a citation plan containing search targets, not invented bibliography entries;
8. known limitations and open evidence gaps.

Use these fields for the claims table: Claim ID, exact claim, evidence and raw path, scope or qualifier, and section.

Use these fields for the positioning table: prior work, its contribution, assumptions and evidence, what this paper adopts or changes, and the distinct project contribution.

Use these fields for each design-chain row: established prior, exposed problem, insufficient default, derived requirement, design response, and predicted observable. If a design response cannot be derived from the preceding fields, remove it from the main story or identify the missing evidence.

Group related work by mechanism or research question. Compare contributions, assumptions, and evidence; do not produce a paper-by-paper list.

## Make every section earn its place

- Put the problem, gap, approach, strongest supported result, and contribution in the abstract and introduction plan. This early payoff does not waive local forward order in the method exposition.
- Assign every experiment or theorem to a claim. Remove results that support no paper claim.
- Give every figure one complete-sentence takeaway, the visual comparison that reveals it within three seconds, and a source. Omit boxes, arrows, panels, and labels that do not support that takeaway.
- Keep one coherent story. Move secondary mechanisms, proofs, and diagnostics to the appendix when they are not needed to understand the main contribution.

Allocate prose to missing or wrong reader priors and non-obvious transitions. Give field consensus one sentence unless the paper disputes it. A planned paragraph should advance one inference; do not make a section or paragraph a bucket of loosely related topics.

If a headline claim lacks evidence, narrow or remove it and add a concrete entry to paper/OPEN_EVIDENCE_GAPS.md. Do not create a second completion contract or ask a reviewer for a numeric rating of the outline.
