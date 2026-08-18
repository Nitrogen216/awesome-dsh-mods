---
name: paper-write
description: Draft or revise a modular LaTeX research paper from an approved claims-evidence plan, verified literature, raw results, and reproducible figures. Use for section-by-section manuscript writing, related-work synthesis, bibliography construction, terminology consistency, and evidence-bounded scientific prose.
---

# Paper Write

Write the paper from paper/PAPER_PLAN.md, not from model memory.

Read `../../references/paper-forward-logic.md` before drafting. Use the plan's reader-state and design-chain rows as ordering constraints.

## Preserve existing work

Inspect any existing LaTeX structure, style files, bibliography, and local instructions before editing. Make surgical revisions when a manuscript already exists. For a new paper with a named venue, use only its verified official template already available in the project or obtained through an authorized path. For a venue-neutral paper, start from `../../templates/paper/VENUE_NEUTRAL_MAIN.tex.tmpl`. Create modular paper/sections/*.tex, paper/references.bib, and a small notation file only when shared macros are needed.

## Draft section by section

For each section:

1. load the claim IDs, evidence paths, literature sources, figures, and page budget assigned in the plan;
2. make each paragraph one inferential move: claim, needed evidence or mechanism, then consequence for the next move;
3. establish the exposed problem, insufficient default, and derived requirement before introducing each design response;
4. distinguish prior authors' claims, promoted project evidence, and interpretation;
5. keep defined terms and notation stable across text, equations, tables, and captions;
6. place quantitative statements only when their source and scope are known;
7. state limitations where they qualify the claim, not only in the conclusion.

The abstract and introduction must expose the problem, gap, approach, strongest supported result, and distinct contribution early. Related work must synthesize mechanism families and explain the exact difference from the closest work. The method must identify what was adopted, replaced, or modified relative to source papers, but may introduce a component only after the reader knows why it is needed. Experiments must say which claim each comparison tests.

Use one sentence for field consensus unless the argument changes it. Spend explanation on absent or incorrect reader priors, non-obvious distinctions, and causal transitions. Merge short fragments that do not carry a complete inference. Use lists only for truly parallel items or procedures; keep the main argument in connected prose. Prefer familiar words, direct sentences, and concrete mechanisms or quantities over professional-sounding abstractions.

## Verify citations before insertion

Reuse a correct existing entry when available. Otherwise verify title, authors, year, and published venue through a primary bibliographic or publisher source before adding the entry. Prefer the published version over a preprint when appropriate. Never fabricate BibTeX or cite a paper from memory alone.

Keep only entries cited by the manuscript, but do not delete an existing bibliography entry merely because a partial draft has not cited it yet.

## Run one writing pass

After all sections exist:

- extract topic sentences as a reverse outline and repair broken argument order;
- remove generic openings, filler, significance inflation, and ambiguous pronouns;
- keep the subject and main verb close and use concrete metric names rather than vague performance claims;
- flag every design choice whose problem or requirement appears only later, then reorder or remove it;
- combine topic fragments and remove empty technical-sounding terms;
- check that title, abstract, introduction, figures, and conclusion express the same contribution and scope.

If prose cannot truthfully close an evidence gap, record it in paper/OPEN_EVIDENCE_GAPS.md; do not invent a result, theorem, baseline, or citation.
