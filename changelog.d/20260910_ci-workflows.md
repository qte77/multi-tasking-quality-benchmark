### Added

- CI pipeline: `.github/workflows/pytest.yaml`, `ruff.yaml`, `pyright.yaml`,
  `complexipy.yaml` — run on push and on PR-close against `main` (plus a
  weekly schedule and manual dispatch), gating on `make test_all`,
  `make ruff`, `make type_check`, `make complexity` respectively. Only
  CodeQL ran in CI before this.

### Removed

- `.github/workflows/dependabot.yaml` — a misplaced Dependabot config
  (Dependabot config must live at `.github/dependabot.yaml`, not under
  `workflows/`; GitHub Actions ignores it there since it has no `on:`/`jobs:`
  keys). It was also a strict subset of the existing, already-correct
  `.github/dependabot.yaml` (which additionally covers the `github-actions`
  ecosystem).
