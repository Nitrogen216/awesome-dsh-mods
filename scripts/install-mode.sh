#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s [--replace] <mode>\n' "$0" >&2
}

replace=false
if [[ "${1:-}" == "--replace" ]]; then
  replace=true
  shift
fi

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

mode=$1
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd "$script_dir/.." && pwd)
source_dir="$repo_root/modes/$mode"
dsh_home=${DSH_HOME:-"$HOME/.dsh"}
target_root="$dsh_home/.agent-presets"
target="$target_root/$mode"

if [[ ! -f "$source_dir/agent.cordis.yml" ]]; then
  printf 'install-mode: unknown or incomplete mode: %s\n' "$mode" >&2
  exit 1
fi

mkdir -p "$target_root"
stage=$(mktemp -d "$target_root/.${mode}.install.XXXXXX")
backup=

cleanup() {
  if [[ -d "$stage" ]]; then
    rm -rf -- "$stage"
  fi
}
trap cleanup EXIT

cp -R "$source_dir/." "$stage/"
chmod -R go-rwx "$stage"

if [[ -e "$target" ]]; then
  if [[ "$replace" != true ]]; then
    printf 'install-mode: %s already exists; rerun with --replace after reviewing local changes\n' "$target" >&2
    exit 1
  fi
  backup="$target.backup.$(date +%Y%m%d%H%M%S)"
  mv "$target" "$backup"
fi

if ! mv "$stage" "$target"; then
  if [[ -n "$backup" && ! -e "$target" ]]; then
    mv "$backup" "$target"
  fi
  exit 1
fi

trap - EXIT
printf 'Installed %s at %s\n' "$mode" "$target"
if [[ -n "$backup" ]]; then
  printf 'Previous copy saved at %s\n' "$backup"
fi
