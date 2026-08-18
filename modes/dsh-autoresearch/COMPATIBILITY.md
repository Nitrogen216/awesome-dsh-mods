# Compatibility

## Initial import

- Imported: 2026-08-18
- DeepSeek Harness source checkout: `47f943859bef60e4160492346772ded9b24f765a`
- DeepSeek Harness tracked upstream at import: `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`
- Base preset: `apps/cli/config/agent-presets/code/agent.cordis.yml`
- ARIS source commit: `0c65f8b34668c39f391b871ac61479eb64497c37`

The source checkout was 111 commits behind its tracked `origin/master` when this repository was created. This records provenance; it does not claim compatibility with every intervening Harness commit.

## Known upstream drift

The tracked upstream `code` preset replaced the product reviewer rows' `enableRunInBackground: false` with `backgroundMode: one-shot`. The imported mode retains the former setting. The tracked implementation accepts both fields, but they select different behavior for explicit background calls.

The tracked upstream also requires production Profiles to install and mount optional Codex or Claude Code providers on the Host Plane. The mode contributes their tool rows only; it does not own those providers.

## Upgrade procedure

1. Compare `agent.cordis.yml` with the target Harness `code` preset.
2. Reconcile upstream row and config changes without discarding mode-specific persona, skill isolation, transition policy, or Oracle authorization.
3. Run the Python and Node tests documented in `README.md`.
4. Mount the preset in a fresh session and verify its model-visible tool catalog.
5. Record the validated Harness commit below before publishing the mode update.

## Validated versions

| Harness commit | Validation | Notes |
|---|---|---|
| `47f943859bef60e4160492346772ded9b24f765a` | Imported local baseline | Full mode files originated from this checkout; repository tests are recorded in the importing commit. |
