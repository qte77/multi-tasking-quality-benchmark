### Added

- `WakaLoader` implementation (`src/mtqb/loader.py`): `load_summaries`,
  `load_projects`, `load_all_time`, `load_durations(date)` — reads
  `waka-data/` JSON files, unwraps `{"data": [...]}` envelopes, validates
  entries with the existing Pydantic models, and raises `FileNotFoundError`
  for missing files/dates. `all_time.json` is read as a flat object (no
  envelope). `data_dir` is fully configurable via `__init__`, no hardcoded
  paths.
- All 7 `xfail(strict=True)` TDD-red tests in `tests/mtqb/test_loader.py`
  turned GREEN; xfail markers removed now that behavior is real.
- `make waka-load` Makefile target (`Makefile.python`): instantiates
  `WakaLoader` against the `WAKA_DATA_DIR` env var (default `../waka-data`)
  and prints a one-line summary of counts loaded.
