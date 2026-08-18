---
name: literature-research
description: Deeply search and read related papers and official implementations for a performance-improvement pipeline. Use after baseline establishment, when a screening or confirmation result shows no gain, when the mapped pool is exhausted, or when a new failure signature is not explained by the current literature map.
---

# Literature Research

Search for mechanisms that address the measured baseline failure, not merely papers sharing task keywords.

## Start with the project's knowledge, then search

1. Inspect the repository's papers, bibliography, literature notes, prior implementation references, and existing synthesis before web discovery. For a broad-direction entrance, also read `research/PROBLEM_ANCHOR.md` and the strongest runnable reference. Reuse a verified local source instead of searching for it again.
2. Start the external search from the method, task, metric, observed failure signature, and the source paper behind the current candidate.
3. Expand through the closest papers' references, citations, terminology, and official code. On refresh, add the rejected mechanism, its failed assumption, and the new failure signature to the query.
4. Prefer primary papers, supplements, and official repositories. Use survey prose only to discover primary sources.
5. Use `web_search` for discovery, then read local PDFs, public full text, supplements, or official repositories. Download an open-access paper through the shell only when its public URL is known and the environment permits it.
6. Read full methods, equations or algorithms, ablations, limitations, and implementation details. Mark abstract-only evidence explicitly and never count it as a deep read.

Build a bounded corpus around the failure rather than satisfying a paper-count quota. Deep-read at least the closest four papers when available, and continue only while a distinct mechanism family, conflicting assumption, or unresolved transfer question remains. Stop when another paper would not change the contribution map; record the search paths tried when the area is sparse.

Independent discovery and paper extraction may run in parallel. Give every source a stable DOI, arXiv id, or normalized title id. The parent executor deduplicates by those ids, resolves version aliases, synthesizes the evidence, and writes `research/LITERATURE.md` once. Delegated readers return source facts and labelled inferences; they do not select the candidate or edit canonical research state.

## Extract transferable contributions

For every deep-read paper, record:

- stable id, verified citation, and source link;
- exact contribution and what it changes relative to its baseline;
- mechanism and required assumptions;
- evidence from ablations or controlled comparisons;
- training and evaluation conditions;
- official implementation touchpoints when available;
- limitation or failure regime;
- plausible insertion, replacement, or adaptation point in the current method;
- what must differ in this project for the adaptation itself to be a contribution.

Distinguish author claims from your inference. Verify bibliographic metadata before relying on it.

## Synthesize around the failure

Write `research/LITERATURE.md` as a revisioned synthesis. Group papers by mechanism, compare their assumptions with `research/BASELINE.md`, identify conflicts, and state which contributions plausibly address the failure profile. For a broad direction, identify the closest prior combination and state the concrete distinction a project-specific adaptation would need to preserve. Keep authors' stated claims separate from the executor's transfer inference. On a refresh, clearly mark new sources, the failed assumption that motivated the search, and how the evidence changes the candidate space.

Do not use Oracle as a substitute for paper search, deep reading, citation verification, or contribution extraction. The mapping phase owns any major unresolved choice between mechanism families. Do not run a general audit. Advance `literature -> mapping` with outcome `literature_ready` only after the synthesis can support concrete hypotheses.
