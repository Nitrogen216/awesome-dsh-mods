---
name: experiment-bridge
description: Execute the active dsh_autoresearch adaptation and experiment plan through DSH-native background jobs. Use in adaptation, screening, or confirmation to implement the selected candidate, detect the configured local or remote compute backend, run a sanity check, reserve stable run IDs, launch training, collect raw results, and hand completed evidence to experiment-run for routing.
---

# DSH-Native Experiment Bridge

Bridge the scientific plan to real execution. `minimal-adaptation` owns the code change, `experiment-plan` owns the comparison and decision rule, and `experiment-run` owns completed-result routing; this skill owns the operational path between them.

## Resolve the current phase and backend

Read `research/STATE.json` through `transition_guard.py show`, the research contract, adaptation record, experiment plan, project `AGENTS.md`, and documented environment commands.

Use the backend the project actually configures:

- local CUDA, MPS, or CPU;
- an explicit SSH host and remote working directory;
- Vast.ai or Modal only when the project supplies that configuration and the required CLI is available.

Never silently switch backend. Do not create a cloud instance, spend a materially larger budget, push commits, destroy resources, or add credential-bearing integrations without the authority already present in the user's request or project instructions. Never expose secrets in commands or logs.

## Implement and prove the path cheaply

In `adaptation`, load `minimal-adaptation`, implement one candidate, run focused tests, and execute the smallest end-to-end smoke that reaches the changed path. Advance to `screening` only when the implementation is runnable and attributable.

In `screening` or `confirmation`, load `experiment-plan` and verify that it names the claim, fixed baseline, single changed variable, metric, seeds, budget, pass rule, invalid-run rule, launch command, backend, and raw output path.

Before a scientific run:

1. verify the environment and required data paths;
2. verify device availability with the backend's ordinary read-only command;
3. run a bounded sanity command that exercises loading, one forward/backward step when applicable, evaluation, and result serialization;
4. fix a concrete implementation or infrastructure failure from its primary log; never rerun an unchanged deterministic failure;
5. stop before full deployment if the sanity result cannot be trusted.

## Reserve and launch one attributable run

Reserve the run ID from the canonical state immediately before launch:

```bash
python3 <preset>/tools/transition_guard.py reserve-run <root>
```

Use that returned ID in the config, log name, raw output path, and `research/RESULTS.jsonl` record. Do not invent another ID or compute a hash. On recovery, inspect the last reserved run, DSH job list, log, and raw output before reserving or launching again.

Launch long work with the DSH bash tool's `run_in_background: true`. Record the returned DSH job ID beside the scientific run ID in `research/EXPERIMENT_PLAN.md`; the job ID controls the process, while the run ID identifies the scientific evidence. Use the job tools and completion notices. Never busy-poll.

Run only one active candidate. Seeds or fixed confirmation replicas for that candidate may run concurrently when the plan and available devices permit it; do not mix candidate mechanisms in one launch wave.

## Collect and route

When completion wakes the session:

1. collect the terminal job result and primary log;
2. verify expected raw files exist and distinguish infrastructure failure from a completed scientific comparison;
3. recompute the declared metric from raw outputs when practical;
4. append one factual result per run to `research/RESULTS.jsonl`, including run ID, DSH job ID, candidate, phase, commit, config, command, backend, split, seed, budget, raw paths, metric, and validity;
5. load `experiment-run` to apply the precommitted screening or confirmation route.

Infrastructure failure before a scientific result keeps the same candidate and decision rule. A valid negative result follows the literature or unused-candidate route and never triggers an automatic Oracle call.
