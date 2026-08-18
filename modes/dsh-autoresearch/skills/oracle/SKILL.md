---
name: oracle
description: "Execute one runtime-authorized browser ChatGPT Pro consultation for a direct user request or an unresolved major decision admitted by askgpt-governor. In dsh_autoresearch, never use Oracle automatically for routine review, implementation, debugging, negative-result analysis, monitoring, tuning, literature retrieval, integrity checks, or prose polish."
---

# Oracle Browser Pro Consultation

Obtain one advisory second opinion with a small, decision-specific evidence bundle. This mode-local skill exposes the `oracle_governor` runtime path; direct Oracle CLI construction is prohibited.

## Enforce the routing contract

- For an automatic call from another skill, require an `askgpt-governor` verdict of `consult_oracle`, then call `oracle_governor` with basis `major_decision`. If the reasoning gate or runtime tool returns `continue_local`, return to the calling skill.
- For a direct user request for Oracle or web ChatGPT Pro, call `oracle_governor` with basis `explicit_user_request` and quote the relevant text from the current human message. This bypasses only automatic eligibility; it does not bypass the bounded decision packet or runtime route.
- Require a semantic decision id and a pending choice among two or three alternatives. Do not use Oracle for open-ended brainstorming or general review.
- Consult once per decision id. Reattach a detached or timed-out session; reconsult only when new evidence materially changes the alternatives.
- Return advisory reasoning to the calling skill. Do not modify pipeline state, authorize user-owned changes, or treat the response as a paper source or experimental result.

## Receive a bounded decision packet

Require the calling skill to provide:

- semantic decision id, such as `mapping:mechanism-family:v1`;
- the exact decision and why it has material consequences;
- two or three scientifically defensible alternatives;
- decisive local baseline, literature, code, and result evidence;
- the uncertainty those sources could not resolve;
- the immediate action that each possible recommendation would change;
- the smallest file paths needed to inspect those facts.

If this packet is incomplete, return to `askgpt-governor` or the calling skill. Do not broaden the task into a general research review.

## Ask the runtime governor, then execute exactly

Call `oracle_governor` with the complete packet. It fixes the signed-in browser route, GPT-5.6 Sol model, Pro thinking tier, prompt form, and file list. Do not write a shell command by hand.

If it returns `consult_oracle`, run its `dryRunCommand` unchanged through `bash` or `pwsh` in the foreground. This preview uses `--dry-run summary --files-report` and does not contact ChatGPT. If it fails, report Oracle as unavailable and return to the calling skill.

After the dry-run succeeds, run its `runCommand` unchanged with `run_in_background: true`. Record the background job id and let the normal job completion event wake the session. Do not busy-poll, prepend wrappers, append flags, or start a duplicate.

Explicit Pro effort fails closed if Pro cannot be confirmed. Availability is account-dependent, and a visible `Pro` picker label alone does not prove the server-side generation tier. If login, account entitlement, picker selection, or CLI validation fails, report Oracle as unavailable and return to the calling skill. Responses remain advisory.

For an automatic consultation, do not use API mode, GPT-5.5, base-Sol `extra-high`, a weaker thinking tier, manual paste, Deep Research, or any fallback. Only an explicit user instruction may override this route.

## Attach evidence safely

- Submit one to eight literal workspace-relative files that contain the decision facts. The runtime tool rejects absolute paths, globs, parent traversal, and credential-like paths.
- Inspect size and token use in the authorized dry-run; keep total input below the CLI limit.
- Never attach `.env` files, private keys, credentials, auth tokens, unpublished protected data, or unrelated artifacts.
- State the project, evaluation protocol, exact alternatives, prior attempts, constraints, and requested output in the prompt because Oracle starts with no project memory.

Ask for one recommendation, the decisive reason, the strongest risk, evidence that would reverse the recommendation, and the smallest next action. Do not request a score or broad failure-mode analysis.

## Verify and hand back

Treat responses as advisory. Verify paper claims and citations against primary sources and technical claims against local code, raw results, and tests. The calling skill owns the final decision and its normal transition rules.

Record only the decision id, Oracle session reference, concise recommendation, and the executor's local decision in the artifact that already owns the choice. Do not create a separate advisor ledger, compute a content hash, or repeatedly audit the same response.

If a run detaches or times out, use the read-only `oracle status --hours 72` and `oracle session <id> --render` commands to inspect or reattach. The runtime guard allows these recovery commands but rejects a duplicate request.
