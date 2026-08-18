---
name: experiment-monitor
description: Check the status and collect the completion signal of an already-running screening or confirmation job. Use for explicit monitoring or when a job event wakes the session; never use monitoring alone to advance the research pipeline.
---

# Experiment Monitor

Inspect the registered background job and its latest logs without changing scientific state.

- Resolve the DSH background job id recorded by `experiment-bridge`; do not treat the scientific run id as a process handle.
- Report running, completed, failed, or missing status with the last meaningful metric or error.
- Wait for job events or use bounded checks; never busy-poll.
- Do not create a new goal round, increment an attempt, reject a candidate, change phase, or call a reviewer based on partial logs.
- When the job completes, hand the raw artifact paths to `experiment-run` for metric collection and routing.
- When infrastructure fails before a scientific result exists, preserve the same candidate and plan while fixing the launch issue.
