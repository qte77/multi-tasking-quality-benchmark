### Security

- Pin every `uses:` in `.github/workflows/*` to a full commit SHA
  (`actions/checkout`, `astral-sh/setup-uv`,
  `github/codeql-action/{init,autobuild,analyze}`), matching the repo's
  `sha_pinning_required` Actions policy. Fixes the CodeQL workflow
  startup failure on `main` since 2026-11-09 and the resulting code
  scanning configuration error.
- Bump `github/codeql-action` to v4.39.3 (supersedes #32).
- Bump `certifi` to 2026.10.23 in `uv.lock`, resolving Dependabot alert
  #3 (critical: emSign root CAs with compromised intermediate CA keys)
  (supersedes #31).

### Changed

- `.github/dependabot.yaml`: add `security-updates`/`version-updates`
  groups for the `pip` and `github-actions` ecosystems, plus a
  dedicated `github-codeql-action` group, so related bumps land in one
  PR instead of one per dependency.
