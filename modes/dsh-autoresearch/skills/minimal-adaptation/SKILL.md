---
name: minimal-adaptation
description: Design and implement the smallest attributable, literature-grounded change for one selected candidate. Use in the adaptation phase after contribution mapping and before any screening training.
---

# Minimal Adaptation

Implement one selected candidate without freezing the entire research direction.

## Specify before editing

Write `research/ADAPTATION.md` with:

- active candidate id and source paper or papers;
- source contribution and assumptions;
- exact project-specific modification;
- expected causal path to the primary metric;
- files and interfaces to change;
- unchanged baseline components;
- screening observables and pass threshold;
- rollback path.

The adaptation may add, replace, or integrate one coherent primitive. Do not attach unrelated rescue modules or tune multiple alternatives in one implementation.

Do not call Oracle for code structure, interfaces, debugging, or implementation details. If implementation reveals a fork that changes the mapped hypothesis or mechanism family, return to `mapping`; that phase owns any major-decision escalation through `askgpt-governor`.

## Implement narrowly

1. Read the relevant architecture and project instructions.
2. Make the smallest source, config, and documentation change that realizes the mapped hypothesis.
3. Preserve the fixed evaluation protocol and protected split.
4. Add focused unit or component tests for the new behavior.
5. Run a smoke test that exercises the changed path without using the screening result to tune it.
6. Record the implementation diff and any deviation from the paper.

Do not launch full training here. Advance `adaptation -> screening` with outcome `implemented` only when the candidate is runnable and attributable. If the mechanism cannot be implemented as mapped, return to `mapping` with outcome `invalid`; refresh literature if the assumption itself was wrong.
