---
name: promotion-review
description: Perform the final promotion decision after a candidate passes full-budget confirmation. Use in the promotion phase to audit evidence, freeze the supported method, or route a failed audit back to confirmation, mapping, or literature.
---

# Promotion Review

Promote only confirmed full-budget evidence.

## Review

1. Run `evidence-audit` against the baseline, frozen candidate, full results, and proposed claim.
2. Confirm that screening did not use held-out evidence for final selection.
3. Bound the claim to the datasets, splits, seeds, budgets, and metrics actually tested.
4. Summarize the method contribution relative to the source papers and the previous baseline.
5. Record the reproducibility receipt as commit, config, command, split, seeds, environment, and raw-result paths.
6. Write a result-to-claim table with the exact supported claim, claims not supported, missing evidence, the revised bounded wording, and the smallest next evidence that would change the decision.

Independent reviewers strengthen assurance but are not an authority over ordinary research transitions. Disclose unavailable providers without blocking a locally supported decision.

If the completed deterministic audit leaves two scientifically defensible promotion or claim-scope decisions and the choice materially changes what will be frozen, load `askgpt-governor` once before deciding. Do not escalate a clear `audit_pass`, `audit_fix`, or `audit_fail`, and never let Oracle override an integrity finding.

## Decide

- For `audit_pass`, apply `promotion -> frozen` with outcome `audit_pass`. Pass `--evidence-id` only when preserving an existing external evidence id. Record the guard-returned canonical evidence id and report the promoted method, primary-metric delta, uncertainty, contribution, bounded claim, unsupported extensions, limits, and artifact paths. If the returned `next_action.skill` is `paper-writing`, load it immediately with the returned target venue; do not complete a paper goal at `frozen`.
- For `audit_fix`, apply `promotion -> confirmation` with outcome `audit_fix` and perform only the named correction or rerun.
- For `audit_fail`, apply `promotion -> mapping` or `promotion -> literature` with outcome `audit_fail`, depending on whether a mapped candidate remains.
- Do not freeze or write a performance claim from screening evidence alone.
