# AGENTS.md — multi-tasking-quality-benchmark

Correlate WakaTime coding activity with code quality metrics.

## Rules

Follow `.claude/rules/` for all work in this repo:

- `core-principles.md` — KISS, DRY, YAGNI, KISS; always-on constraints
- `context-management.md` — keep context 40-60%, compact after phase transitions
- `testing.md` — AAA structure, tmp_path, mirror src/ in tests/

## Workflow

```bash
make validate   # ruff + pyright + complexipy + pytest --cov (run before every commit)
make test_all   # pytest only
make type_check # pyright only
```

## TDD Policy

- **Behavior tests only** — test what the module does, not how it does it
- **Non-trivial tests only** — do NOT test declarative Pydantic models, ABCs,
  or simple scripts; test modules that contain real logic
- **RED before GREEN** — write failing tests first, then implement to pass them
- **Fixtures over mocks** — use committed JSON fixtures under `tests/mtqb/fixtures/`
  for file-based tests; use `tmp_path` for filesystem isolation
- **No hardcoded paths** — never use `/workspaces/` in tests (breaks CI)

## Data

`waka-data/` is external and gitignored. Tests use committed fixtures at
`tests/mtqb/fixtures/`. Run `make waka-poll` to fetch real data locally.
