---
name: experiment-run
description: Collect, compare, and route screening or confirmation results launched through the DSH-native experiment bridge. Use only after a plan exists and experiment-bridge has reserved a scientific run id and launched or completed the background job.
---

# Experiment Run

Consume the precommitted bridge run and turn the completed result into the next pipeline route. `experiment-bridge`, not this skill, owns backend selection, run-id reservation, and launch.

## Launch and collect

1. Verify the phase, active candidate, plan, baseline artifact, reserved scientific run id, output path, device rules, and DSH job completion.
2. Persist the DSH background job id separately from the scientific run id, plus the exact command, config, commit, split, seed, budget, and raw-result path.
3. Let job completion events wake the session. Do not busy-poll or advance scientific state for a status check.
4. On completion, recompute the declared metric from raw outputs when practical and append one factual record to `research/RESULTS.jsonl`.

Do not modify the candidate or decision threshold after seeing a result.

## Route screening

- If the precommitted threshold and guardrails pass, apply `screening -> confirmation` with outcome `screen_pass`.
- If a valid run has no gain, append a concise rejection record and apply `screening -> mapping` with outcome `screen_fail` when an unused mapped candidate directly fits. Otherwise apply `screening -> literature` with outcome `screen_fail`.
- If the run is invalid because of a bug or infrastructure failure, fix the same implementation and rerun only when the scientific comparison was never observed. Use outcome `invalid` when leaving the candidate.

## Route confirmation

- If the frozen candidate passes the full promotion rule, apply `confirmation -> promotion` with outcome `confirmed`.
- If the gain disappears, is unstable, or violates a guardrail, apply `confirmation -> mapping` or `confirmation -> literature` with outcome `not_confirmed`.
- Never promote a screening-only result.

For an ordinary no-gain result, limit interpretation to the metric delta, uncertainty, failed assumption, validity, and next route. Do not launch a general audit or spend further rounds defending the candidate.

A valid `screen_fail` or `not_confirmed` result follows the routes above and is not an Oracle trigger. Load `askgpt-governor` only when completed evidence exposes a protocol-level contradiction or research-program fork whose resolution materially changes the objective, evaluation obligations, or remaining compute. Never use Oracle to reinterpret a failed result into a pass.
