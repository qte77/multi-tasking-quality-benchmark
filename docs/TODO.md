---
title: TODO - multi-tasking-quality-benchmark
description: Task tracker for the WakaTime quality correlation pipeline
category: implementation
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
---

# TODO: multi-tasking-quality-benchmark

## Done

- [x] WakaTime data collection — `../waka-data/` has 14 days of real data
      (summaries, durations, projects, all_time)
- [x] Repo created
- [x] Foundational docs: README, UserStory, architecture, TODO

## Next

- [ ] Pydantic models for `waka-data/` JSON schemas (`WakaSessionData`,
      `WakaSummary`, `QualitySnapshot`, `CorrelationRecord`)
- [ ] Data loader (`src/waka/loader.py`) — read existing `waka-data/` files
      into models without API calls
- [ ] Quality collector (`src/waka/quality_collector.py`) — ruff + pyright +
      pytest + complexipy + jscpd → `QualitySnapshot`
- [ ] `make waka-load` and `make quality-snapshot REPO=path` Makefile targets
- [ ] Unit tests for models and loader (mock filesystem, no API calls)

## Backlog

- [ ] WakaTime client (`src/waka/client.py`) — httpx, HTTP Basic auth,
      rate limiting, poll → `waka-data/`
- [ ] `make waka-poll` Makefile target
- [ ] Correlator (`src/waka/correlator.py`) — join activity + quality
      snapshots → `CorrelationRecord` list
- [ ] `make waka-correlate` Makefile target
- [ ] Correlation report writer — `results/correlation.md` + `results/data.csv`
- [ ] Session tagger (`src/waka/session_tagger.py`) — `.wakatime-project`
      write/restore context manager, tag format `S01/cc/phase1`
- [ ] Integration with `coding-agent-eval` — tag agent runs, pull quality
      snapshots, compare human vs agent sessions
- [ ] `pyproject.toml` with project metadata and dev dependencies (ruff,
      pyright, pytest, complexipy, jscpd)
- [ ] `Makefile` with full command surface

## Deferred

- [ ] Wakapi self-hosted server setup
- [ ] WakaTime paid tier backfill automation (full history beyond 14 days)
- [ ] Statistical significance testing (exploratory only for now)
- [ ] Visualization dashboards or interactive charts
- [ ] CI/CD pipeline
