---
title: TODO - multi-tasking-quality-benchmark
description: Task tracker for the WakaTime quality correlation pipeline
category: implementation
created: 2026-03-22
updated: 2026-09-10
version: 1.2.0
---

# TODO: multi-tasking-quality-benchmark

## Done

- [x] Repo created
- [x] Foundational docs: README, UserStory, architecture, TODO, decisions
- [x] Repo scaffold to estate standard: `pyproject.toml`, `Makefile`,
      `Makefile.python`, `.editorconfig`, `.gitignore`, `LICENSE` (MIT),
      `SECURITY.md`, `AGENTS.md`, `.claude/rules/`, `.claude/skills/`
- [x] Pydantic models (`src/mtqb/models.py`): `SummaryProject`, `DailySummary`,
      `Project`, `AllTime`, `DurationSegment`; all `strict=True, frozen=True`
- [x] WakaLoader interface stub (`src/mtqb/loader.py`): typed signatures,
      `NotImplementedError` bodies, full docstrings
- [x] Loader spec tests (`tests/mtqb/test_loader.py`): 7 `xfail(strict=True)`
      TDD-red tests + 1 fixture sanity test; committed fixtures under
      `tests/mtqb/fixtures/`
- [x] `WakaLoader` logic implemented (`src/mtqb/loader.py`): `load_summaries`,
      `load_projects`, `load_all_time`, `load_durations(date)` — unwraps
      `{"data": [...]}` envelopes, validates with Pydantic, raises
      `FileNotFoundError` on missing files; all 7 spec tests turned GREEN
      (xfail markers removed)
- [x] `make waka-load` Makefile target (`Makefile.python`): instantiates
      `WakaLoader` against `WAKA_DATA_DIR` (default `../waka-data`) and
      prints a one-line summary of counts loaded

## Phase 0 Checklist

- [ ] `waka-data/` external data store present (NOT in-repo; fetch via `make waka-poll`)
- [x] Loader logic implemented (`src/mtqb/loader.py`, no longer a stub)

## Backlog

- [ ] Quality collector (`src/mtqb/quality_collector.py`) — ruff + pyright +
      pytest + complexipy + jscpd → `QualitySnapshot`
- [ ] `make quality-snapshot REPO=path` Makefile target
- [ ] Correlator (`src/mtqb/correlator.py`) — join activity + quality
      snapshots → `CorrelationRecord` list
- [ ] `make waka-correlate` Makefile target
- [ ] Correlation report writer — `results/correlation.md` + `results/data.csv`
- [ ] WakaTime client (`src/mtqb/client.py`) — httpx, HTTP Basic auth,
      rate limiting, poll → `waka-data/`
- [ ] `make waka-poll` Makefile target
- [ ] Session tagger (`src/mtqb/session_tagger.py`) — `.wakatime-project`
      write/restore context manager, tag format `S01/cc/phase1`
- [ ] Integration with `coding-agent-eval` — tag agent runs, pull quality
      snapshots, compare human vs agent sessions

## Deferred

- [ ] Wakapi self-hosted server setup
- [ ] WakaTime paid tier backfill automation (full history beyond 14 days)
- [ ] Statistical significance testing (exploratory only for now)
- [ ] Visualization dashboards or interactive charts
- [ ] CI/CD pipeline
