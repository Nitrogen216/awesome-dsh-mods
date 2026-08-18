---
name: evidence-audit
description: Audit confirmed evidence for integrity, reproducibility, and result-to-claim support before promotion, or investigate a concrete anomaly that could change a decision. Do not trigger it after every ordinary screening failure.
---

# Evidence Audit

Audit decision-relevant evidence without turning assurance into the research loop.

## Use the narrow audit surface

For promotion, inspect:

- the fixed baseline and candidate commits;
- config, split, preprocessing, seeds, commands, and raw result paths;
- metric recomputation and aggregation;
- leakage, accidental test selection, missing cases, and failed runs;
- whether the implementation matches `research/ADAPTATION.md`;
- whether the full-budget result supports the proposed bounded claim.

For a concrete anomaly, inspect only the evidence needed to resolve it.

Do not use Oracle to decide metric correctness, leakage, reproducibility, or other evidence facts. Complete the deterministic audit first; `promotion-review` owns any later escalation when valid evidence still permits materially different promotion or claim-scope decisions.

## Use reviewers as optional independent evidence

Run a fresh Codex or Claude Code review when available and when its result can change promotion. Give the reviewer source and artifact paths plus a neutral question. Do not require both providers, and do not substitute a weaker provider while claiming equivalent assurance. If a provider is unavailable, record the limitation and complete the deterministic local audit.

## Record the verdict

Write `research/PROMOTION_AUDIT.md` with one verdict:

- `audit_pass`: evidence is valid, reproducible, and supports the bounded claim;
- `audit_fix`: evidence or reporting needs a defined correction or rerun;
- `audit_fail`: the confirmed claim is unsupported or the comparison is invalid.

Record commit, configs, split, seeds, commands, and raw paths. You may propose an external evidence label when one already exists, but the transition guard owns the canonical promotion evidence id and generates it by default.
