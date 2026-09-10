### Added

- `CONTRIBUTING.md`: filled in from the estate template
  (`qte77/qte77` doc-structure canon) with this repo's actual commands
  (`make validate_quick`, `make test_all`, `make lint_md`, `make lint_links`),
  changelog mechanism (scriv fragments under `changelog.d/`), and release
  process (`bump-my-version` + `scriv collect`).
- `AGENT_LEARNINGS.md`, `AGENT_REQUESTS.md`: estate-standard governance
  scaffolding (empty templates — accumulate over time per
  `.claude/rules/compound-learning.md`).
- `MEMORY.md`: project-scoped Claude Code memory seed (empty template).
- `.claude/rules/testing.md`: testing conventions rule file (mock external
  deps, arrange/act/assert, mirror `src/` in `tests/`, `tmp_path` isolation)
  — already followed in `tests/mtqb/test_loader.py`, now codified.
- `.scaffolds/python.sh`, `.scaffolds/extract_signatures.py`: Ralph-loop
  Python adapter scripts (test/lint/typecheck/complexity/coverage wrappers
  around the existing `make`/`uv` commands, plus AST-based Python signature
  extraction).
