### Added

- Quality collector (`src/mtqb/quality_collector.py`): runs ruff, pyright,
  pytest, complexipy and jscpd against a target repo and returns a
  `QualitySnapshot` (new model in `src/mtqb/models.py`). A missing tool, a
  timeout or unparseable output yields `None` for that metric, so partial
  snapshots are valid (#2).
- `make quality-snapshot REPO=path` Makefile target: prints the snapshot as
  JSON.
