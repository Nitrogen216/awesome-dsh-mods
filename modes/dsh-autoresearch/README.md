# dsh-autoresearch

`dsh-autoresearch` is a research-oriented mode derived from the DeepSeek Harness `code` preset. It organizes existing-project improvement, broad-direction convergence, experiment screening, full-budget confirmation, evidence promotion, and paper delivery as a resumable V4 pipeline.

## Components

- `agent.cordis.yml` defines the Agent Plane composition, persona, tools, and runtime policies.
- `skills/` contains 21 mode-private skills and isolates the mode from the default skill roots.
- `plugins/skill-isolation.mjs` restricts automatic skill loading to the curated mode catalog.
- `plugins/oracle-governor.mjs` restricts Oracle execution to the authorized browser-based Pro route.
- `tools/transition_guard.py` persists and validates research-stage transitions.
- `templates/` and `references/` provide research and paper-delivery artifacts.
- `vendor/aris-upstream/` contains a pinned snapshot of upstream ARIS files.

## Install on macOS

Install Node.js and Git as described in the [repository prerequisites](../../README.md#prerequisites), then run from the repository root:

```sh
./scripts/install-mode.sh dsh-autoresearch
npx @deepseek-ai/dsh web
```

## Install on Windows

Install Node.js and Git as described in the [repository prerequisites](../../README.md#prerequisites), then run from the repository root in PowerShell:

```powershell
.\scripts\install-mode.ps1 -Mode dsh-autoresearch
npx @deepseek-ai/dsh web
```

Open `http://127.0.0.1:3080`, create a new session, and select `dsh-autoresearch` from the Agent Preset picker. Machine-local credentials, model selection, and browser sign-in state must be configured separately on each computer.

## Optional local dependencies

- The Oracle route requires an `oracle` executable and browser access to the requested ChatGPT Pro capability.
- `subagent_codex` and `subagent_claude_code` require the active Profile to install and mount their providers on the Host Plane. The main research pipeline remains available without those optional external reviewers.
- Long-running training jobs depend on the target project's own Python, GPU, and SSH environment.

## Validation

Run the static policy and transition-state tests from the `awesome-dsh-mods` repository root:

```sh
python3 -B -m unittest discover -s modes/dsh-autoresearch/tools/tests -p 'test_*.py'
```

Run the runtime plugin tests from a built DeepSeek Harness checkout:

```sh
cd <deepseek-harness>
node --test /absolute/path/to/awesome-dsh-mods/modes/dsh-autoresearch/tools/tests/test_runtime_plugins.mjs
```

After a Harness upgrade, also start a fresh `dsh-autoresearch` session and verify preset mounting, the isolated skill catalog, Code Mode, background jobs, and any optional reviewer providers.
