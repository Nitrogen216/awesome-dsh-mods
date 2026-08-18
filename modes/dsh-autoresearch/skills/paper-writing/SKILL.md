---
name: paper-writing
description: Orchestrate evidence-bounded research paper writing from promoted results or an existing manuscript. Use when the user explicitly asks for a paper, manuscript, LaTeX, or PDF, or when V4 frozen state returns next_action.skill paper-writing; coordinate planning, figures, drafting, compilation, bounded revision, and one final factual check without restarting research.
---

# Paper Writing Pipeline

Turn stable research evidence into a clear, source-grounded manuscript. Keep paper production separate from scientific candidate selection.

Before dispatching a paper phase, read `../../references/paper-forward-logic.md`. Its reader-state, paragraph, and figure rules apply to every artifact in this pipeline.

## Accept an explicit or state-directed entrance

- Start this workflow for either a direct paper, manuscript, LaTeX, or PDF request, or a guard-confirmed `frozen` state whose persisted deliverable is `paper` and whose `next_action.skill` is `paper-writing`.
- On a state-directed handoff, preserve the active autonomous goal. Do not create a second goal or mark it complete until `paper/main.pdf` and `paper/FINAL_CHECK.md` exist.
- Use promoted evidence from research/PROMOTION_AUDIT.md when available. An existing paper project with explicit source artifacts is also a valid input.
- If research is not frozen, allow a clearly labelled provisional draft, but do not promote claims or change research state.
- If the request asks for new evidence or model improvement, finish that work through depth-research-loop before treating the result as paper evidence.

Resolve the venue once. Use the direct human request when it names a venue; otherwise use the persisted `target_venue`. If neither names one, set the writing target to `venue-neutral` and continue through a complete compilable research article. Do not stop to request a venue and do not invent venue rules.

## Follow one writing path

    evidence handoff -> claims and outline -> figures and tables -> section draft
                     -> compile and render -> bounded revision -> final factual check

1. Load paper-plan. Freeze one sentence that states the supported contribution, map every headline claim to promoted evidence and relevant literature, and build the forward problem-to-requirement-to-choice chain.
2. Load paper-figure. Define one three-second takeaway per asset, then generate only the elements needed for it from raw result artifacts or an explicit editable diagram specification.
3. Load paper-write. Draft modular LaTeX section by section using the plan, verified citations, generated assets, and the established reader-state order.
4. Load paper-compile. Build the PDF, diagnose compilation failures, and inspect the rendered pages.
5. Load paper-polish. Run at most two issue-driven revision passes, recompile after material edits, and write the single final factual check.

Do not insert extra review phases between these steps. A failed compile returns to the source location that caused it. A factual gap returns to the claims map, where the claim is narrowed, removed, or recorded as an open evidence gap.

`paper-plan` owns the writing pipeline's only automatic Oracle escalation, and only for a major unresolved choice between scientifically different central contribution framings. Drafting, figures, compilation, and polishing never call Oracle automatically.

## Keep the evidence handoff explicit

Prefer these inputs:

| Input | Use |
|---|---|
| research/PROMOTION_AUDIT.md | Supported claim, scope, confirmed delta, and limitations |
| research/RESULTS.jsonl plus raw result paths | Numbers, uncertainty, tables, and plots |
| research/LITERATURE.md | Prior contributions, assumptions, limitations, and positioning |
| research/CONTRIBUTION_MAP.md and research/ADAPTATION.md | Source-to-project contribution mapping |
| Existing LaTeX and bibliography | Preserve and revise rather than regenerate |

When an input is absent, inspect the repository for an equivalent authoritative source. Never fill a missing result, comparison, citation, or method detail from memory.

State the final payoff early in the title, abstract, and introduction. In the technical body, present the problem and insufficient default before the requirement, and the requirement before the design response. This is forward explanation, not suspense and not retrospective justification.

## Produce a small artifact set

| Artifact | Purpose |
|---|---|
| paper/PAPER_PLAN.md | Claims-evidence matrix, related-work map, section budget, and asset plan |
| paper/sections/*.tex and paper/main.tex | Manuscript source |
| paper/references.bib | Cited and verified bibliography entries |
| paper/figures/ | Reproducible plots, tables, diagram specifications, and rendered assets |
| paper/main.pdf | Current compiled manuscript |
| paper/OPEN_EVIDENCE_GAPS.md | Only gaps that cannot be fixed by truthful writing |
| paper/FINAL_CHECK.md | One human-readable final factual and presentation check |

## Preserve the boundary

- Do not mutate research/STATE.json or research/PIPELINE.jsonl during paper writing.
- Do not launch training, select a new candidate, or change the promoted method from a writing workflow.
- Do not turn review comments into unsupported experiments, claims, citations, or theorem statements.
- Do not run post-submission response or venue-porting workflows.
- Do not build separate acceptance, freshness, forensic, or reviewer-rating ledgers.
- Verify current venue requirements from the official venue source when formatting or page limits matter.
- For `venue-neutral`, use the preset's neutral article template when no project template exists, mark venue-specific checks not applicable, and leave later venue formatting to a separate explicit request.
