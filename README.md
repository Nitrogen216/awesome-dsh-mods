# Awesome DSH Mods

A collection of custom [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Agent Presets. Each mode is a self-contained directory that can be installed under `$DSH_HOME/.agent-presets`.

DeepSeek Harness is currently a developer preview and may introduce compatibility-breaking changes. Each mode therefore carries its own compatibility record and validation instructions.

## Modes

| Mode | Purpose | Status |
|---|---|---|
| [`dsh-autoresearch`](modes/dsh-autoresearch/) | Evidence-bounded autonomous research, experiment promotion, and paper delivery | Active |

## Prerequisites

The [official DeepSeek Harness run guide](https://github.com/deepseek-ai/deepseek-harness#run) starts DSH with `npx @deepseek-ai/dsh web`. Its current Node.js requirement is `^22.19.0 || >=24.0.0`, so install Node.js 22.19 or newer in the Node 22 line, or Node.js 24 or newer. You also need Git.

- [Download Node.js](https://nodejs.org/en/download)
- [Download Git](https://git-scm.com/downloads)

Verify both commands before installing a mode:

```text
node --version
git --version
```

## Install on macOS

Open Terminal and run:

```sh
git clone https://github.com/Nitrogen216/awesome-dsh-mods.git
cd awesome-dsh-mods
./scripts/install-mode.sh dsh-autoresearch
```

The installer copies the mode to `${DSH_HOME:-$HOME/.dsh}/.agent-presets/dsh-autoresearch`. Start DSH using the command from the official guide:

```sh
npx @deepseek-ai/dsh web
```

Open `http://127.0.0.1:3080`, create a new session, and select `dsh-autoresearch` from the Agent Preset picker.

## Install on Windows

Open PowerShell and run:

```powershell
git clone https://github.com/Nitrogen216/awesome-dsh-mods.git
Set-Location awesome-dsh-mods
.\scripts\install-mode.ps1 -Mode dsh-autoresearch
```

The installer copies the mode to `$env:DSH_HOME\.agent-presets\dsh-autoresearch` when `DSH_HOME` is set, or `$HOME\.dsh\.agent-presets\dsh-autoresearch` otherwise. Start DSH using the command from the official guide:

```powershell
npx @deepseek-ai/dsh web
```

Open `http://127.0.0.1:3080`, create a new session, and select `dsh-autoresearch` from the Agent Preset picker.

## Update a mode

### macOS

```sh
git pull --ff-only
./scripts/install-mode.sh --replace dsh-autoresearch
```

### Windows

```powershell
git pull --ff-only
.\scripts\install-mode.ps1 -Mode dsh-autoresearch -Replace
```

Both installers refuse to overwrite an existing mode unless replacement is explicitly requested. Replacement moves the previous installation to a timestamped sibling backup before installing the new copy. Restart DSH after installing or updating a mode.

## Run DeepSeek Harness from source

If you develop against a local Harness checkout, the [official source instructions](https://github.com/deepseek-ai/deepseek-harness#run-from-source) are:

```sh
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

The mode installation path is independent of whether DSH runs through `npx` or from source.

## Repository layout

```text
awesome-dsh-mods/
├── modes/
│   └── dsh-autoresearch/
└── scripts/
    ├── install-mode.sh
    └── install-mode.ps1
```

DSH discovers presets as real directories, so the installers copy a mode instead of creating a symbolic link. User presets are complete configuration snapshots and do not automatically inherit later changes from the official presets. Review the mode's [`COMPATIBILITY.md`](modes/dsh-autoresearch/COMPATIBILITY.md) and rerun its validation steps after upgrading DSH.

Third-party sources and licenses are recorded in each mode's `THIRD_PARTY_NOTICES.md`.
