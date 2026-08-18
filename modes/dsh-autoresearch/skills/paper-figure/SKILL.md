---
name: paper-figure
description: Create reproducible manuscript plots, tables, and editable architecture or workflow diagrams from the paper plan and authoritative result artifacts. Use when a paper needs data figures, comparison tables, multi-panel results, or a deterministic method diagram, including rendered visual verification.
---

# Paper Figures

Generate only assets requested by paper/PAPER_PLAN.md.

Read the figure rules in `../../references/paper-forward-logic.md`. Write one complete-sentence takeaway before drawing each asset.

## Separate evidence figures from diagrams

- For plots and result tables, read raw JSON, JSONL, CSV, TSV, or the project's canonical result files. Never copy values from prose or hardcode result arrays.
- For architecture and workflow diagrams, create an editable SVG or TikZ source. Use the vendored deterministic figure renderer when it fits; do not use a generated illustration unless the user explicitly requests that style.
- Preserve existing user-created figures and their source files.

## Generate reproducibly

For each asset:

1. record its one-sentence takeaway, claim ID, and raw data path;
2. identify the comparison or visual relation that lets a reader extract that takeaway in three seconds;
3. remove every box, arrow, panel, label, and decoration that does not support the takeaway, then establish a clear visual hierarchy;
4. check that compared rows share the evaluation protocol, budget, split, and aggregation;
5. state the unit of replication and uncertainty when a summary is shown;
6. keep the generation script or editable specification next to the output;
7. export vector PDF or SVG when possible;
8. draft a self-contained caption that says what is compared, what the reader should notice, and the scope the evidence supports.

Place outputs under paper/figures/, with scripts or specifications under paper/figures/source/.

## Inspect the rendered artifact once

Open the produced PDF, SVG, or raster output at its intended paper size. First run the three-second takeaway test without relying on the surrounding prose. Then check legibility, clipping, legend overlap, units, grayscale and color accessibility, caption agreement, and consistency with every plotted row. Fix observed defects and rerender.

Do not convert every named method module into a diagram box or every textual dependency into an arrow. When one asset tries to communicate two independent conclusions, split it only if both are claim-bearing; otherwise keep the central takeaway and remove the secondary material.

Do not request an aesthetic rating loop. If a proposed comparison is scientifically incompatible, change the plan or separate the conditions instead of hiding the mismatch with styling.
