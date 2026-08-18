# Awesome DSH Mods

A curated collection of custom Agent Presets (Modes) for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness).

Each mode is a self-contained preset directory that plugs directly into DeepSeek Harness's per-session Agent Plane architecture, mounted under `${DSH_HOME:-$HOME/.dsh}/.agent-presets/`.

---

## Table of Contents

- [Available Modes](#available-modes)
- [Prerequisites](#prerequisites)
- [Quick Start & Installation](#quick-start--installation)
  - [macOS / Linux](#macos--linux)
  - [Windows (PowerShell)](#windows-powershell)
- [Running DeepSeek Harness](#running-deepseek-harness)
- [Updating & Managing Modes](#updating--managing-modes)
- [How Presets Work](#how-presets-work)
- [Authoring a New Mode](#authoring-a-new-mode)
- [Repository Layout](#repository-layout)
- [Compatibility & Upstream Tracking](#compatibility--upstream-tracking)
- [Acknowledgements](#acknowledgements)

---

## Available Modes

| Mode | Base Preset | Status | Purpose & Highlights |
|---|---|---|---|
| [`dsh-autoresearch`](modes/dsh-autoresearch/) | `code` | **Active** | Evidence-bounded autonomous research, hypothesis formulation, baseline assessment, iterative experimentation, promotion audit, and paper delivery pipeline. |

> *More community modes will be added over time. See [Authoring a New Mode](#authoring-a-new-mode) to contribute.*

---

## Prerequisites

DeepSeek Harness requires **Node.js** (`^22.19.0 || >=24.0.0`) and **Git**.

- [Download Node.js](https://nodejs.org/en/download) (Node 22.19+ or Node 24+)
- [Download Git](https://git-scm.com/downloads)

Verify your local environment before installing modes:

```sh
node --version
git --version
```

---

## Quick Start & Installation

### macOS / Linux

Open your terminal and run:

```sh
# 1. Clone the repository
git clone https://github.com/Nitrogen216/awesome-dsh-mods.git
cd awesome-dsh-mods

# 2. Install the desired mode (e.g. dsh-autoresearch)
./scripts/install-mode.sh dsh-autoresearch
```

The installer copies the mode to `${DSH_HOME:-$HOME/.dsh}/.agent-presets/dsh-autoresearch` and configures secure directory permissions (`go-rwx`).

---

### Windows (PowerShell)

Open PowerShell and run:

```powershell
# 1. Clone the repository
git clone https://github.com/Nitrogen216/awesome-dsh-mods.git
Set-Location awesome-dsh-mods

# 2. Install the desired mode (e.g. dsh-autoresearch)
.\scripts\install-mode.ps1 -Mode dsh-autoresearch
```

The installer copies the mode to `$env:DSH_HOME\.agent-presets\dsh-autoresearch` (or `$HOME\.dsh\.agent-presets\dsh-autoresearch` if `DSH_HOME` is unset).

---

## Running DeepSeek Harness

Start DeepSeek Harness with:

```sh
npx @deepseek-ai/dsh web
```

### Accessing the Web UI

1. Open your browser and navigate to `http://127.0.0.1:3080`.
2. Click **New Session** (or connect a workspace).
3. In the **Agent Preset** dropdown picker, select the newly installed mode (e.g., `dsh-autoresearch`).

---

## Updating & Managing Modes

### Updating an Existing Mode

To update an existing mode from the latest repository changes, use the `--replace` (or `-Replace`) flag. The installer will safely move the existing installation to a timestamped backup directory (e.g., `dsh-autoresearch.backup.YYYYMMDDHHMMSS`) before copying the new version:

#### macOS / Linux:
```sh
git pull --ff-only
./scripts/install-mode.sh --replace dsh-autoresearch
```

#### Windows (PowerShell):
```powershell
git pull --ff-only
.\scripts\install-mode.ps1 -Mode dsh-autoresearch -Replace
```

> **Note**: Restart your DeepSeek Harness process after installing or updating a mode so the running server discovers the latest preset generation.

### Uninstalling a Mode

To remove an installed mode, delete its folder from your user preset directory:

```sh
# macOS / Linux
rm -rf "${DSH_HOME:-$HOME/.dsh}/.agent-presets/dsh-autoresearch"

# Windows (PowerShell)
Remove-Item -Recurse -Force "$HOME\.dsh\.agent-presets\dsh-autoresearch"
```

---

## How Presets Work

DeepSeek Harness separates composition into two planes:
- **Host Plane (Process Singleton)**: Owns shared infrastructure (registries, database persistence, session routing, sandbox execution, subagent providers).
- **Agent Plane (Per-Session Preset)**: Owns session-scoped capabilities (tool row presentation, persona, prompt sections, isolated skills, and compaction policies).

### Key Architectural Behaviors

- **Real Directory Copying**: DSH discovers presets as real directories. The installer copies the mode directory rather than creating symlinks, ensuring presets remain self-contained, reproducible snapshots.
- **Dynamic Discovery**: DeepSeek Harness scans `${DSH_HOME}/.agent-presets` dynamically on `list()` and `resolve()` calls without caching.
- **Session Locking**: Once a session begins executing and produces turns, its active preset is locked in the session log to guarantee deterministic replay.

---

## Authoring a New Mode

To contribute or create a new mode in this repository:

1. **Create Mode Directory**: Add a new folder under `modes/<mode-id>/` (the ID must match `^[a-z0-9][a-z0-9-]*$`).
2. **Include Required Components**:
   - `agent.cordis.yml`: Agent Plane Cordis plugin composition.
   - `preset.yml`: Display metadata (`name` and `description`).
   - `README.md`: Mode-specific documentation and dependencies.
   - `COMPATIBILITY.md`: Baseline DSH commit and upstream tracking records.
   - `THIRD_PARTY_NOTICES.md`: Attribution and open-source licenses for bundled assets.
3. **Validate & Test**:
   - Run static policy and integrity tests:
     ```sh
     python3 -B -m unittest discover -s modes/<mode-id>/tools/tests -p 'test_*.py'
     ```
   - Test preset mounting against DeepSeek Harness:
     ```sh
     node --test modes/<mode-id>/tools/tests/test_runtime_plugins.mjs
     ```
4. **Register in Root README**: Add your mode to the [Available Modes](#available-modes) table.

---

## Repository Layout

```text
awesome-dsh-mods/
├── README.md                      # Repository guide and mode catalog
├── modes/                         # Self-contained mode presets
│   └── dsh-autoresearch/          # Autonomous research pipeline mode
│       ├── agent.cordis.yml       # Agent-plane composition
│       ├── preset.yml             # UI display metadata
│       ├── COMPATIBILITY.md       # Upstream compatibility tracking
│       ├── THIRD_PARTY_NOTICES.md # Third-party licenses
│       ├── README.md              # Mode-specific documentation
│       ├── plugins/               # Runtime guard & isolation plugins
│       ├── skills/                # Mode-private skills
│       └── tools/tests/           # Policy and runtime test suites
└── scripts/
    ├── install-mode.sh            # macOS/Linux installer
    └── install-mode.ps1           # Windows installer
```

---

## Compatibility & Upstream Tracking

DeepSeek Harness is actively evolving. User presets are complete configuration snapshots and do not automatically inherit subsequent changes made to the upstream official presets.

- Each mode in this repository maintains a dedicated `COMPATIBILITY.md` recording its baseline upstream commit, known drift, and upgrade procedures.
- Always review the target mode's `COMPATIBILITY.md` and run its test suite after upgrading DeepSeek Harness.

---

## Acknowledgements

- **[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)**: For providing the extensible agent harness framework and Cordis runtime architecture.
- **[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** (Auto-claude-code-research-in-sleep by [@wanshuiyin](https://github.com/wanshuiyin)): Specifically acknowledged for inspiring and providing reference workflows, skills, and paper templates used in the [`dsh-autoresearch`](modes/dsh-autoresearch/) preset.


