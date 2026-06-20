---
title: Architecture - multi-tasking-quality-benchmark
description: System design and component breakdown for the WakaTime quality correlation pipeline
category: technical
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
---

# Architecture: multi-tasking-quality-benchmark

> **Status: Planned Design — no code yet.** This document describes the
> intended architecture. Nothing in `src/` is implemented beyond stubs.

## Overview

A pipeline that reads WakaTime coding activity data, runs code quality tools
against target repos, and joins both datasets into a correlation report.
The WakaTime data store (`../waka-data/`) is external and shared; this repo
consumes it read-only (except during polling).

## Data Flow

```
WakaTime API
     |
     v
[mtqb/client.py] --writes--> ../waka-data/
                                  |
                    +-------------+-------------+
                    |             |             |
               summaries    durations/     all_time
               .json        YYYY-MM-DD     .json
                    |             |
                    +------+------+
                           |
                    [mtqb/loader.py]
                           |
                           v
                  DailySummary / DurationSegment
                           |
                           |
target repo  ------>  [mtqb/quality_collector.py]
                           |
                           v
                      QualitySnapshot
                           |
                           |
                    [mtqb/correlator.py]
                           |
                     CorrelationRecord
                           |
              +------------+------------+
              |                         |
    results/correlation.md        results/data.csv
```

## Components

### WakaTime Client (`src/mtqb/client.py`)

Fetches data from the WakaTime API and persists it to `waka-data/`.

- HTTP library: `httpx`
- Auth: HTTP Basic — API key as username, empty password (`base64(key:)`)
- Key source: parses `~/.wakatime.cfg` for `api_key=`; falls back to
  `WAKATIME_API_KEY` env var
- Rate limiting: 0.2s delay between calls to avoid 429s
- Endpoints used:
  - `GET /api/v1/users/current/summaries` — daily summaries
  - `GET /api/v1/users/current/durations` — per-day duration segments
  - `GET /api/v1/users/current/all_time_since_today` — lifetime totals
- Bulk strategy: omit `&project=` to download all projects in one call,
  filter client-side

### Data Store (`../waka-data/`)

External directory written by the poll command and read by the loader.
Not owned by this repo.

```
waka-data/
  summaries.json          # daily aggregated stats
  projects.json           # project list
  all_time.json           # lifetime totals; daily_average in seconds
  durations/
    YYYY-MM-DD.json       # one file per day, list of duration segments
```

Free tier retains 14 days. Outside that window, API returns `{"data": []}`.

### Data Loader (`src/mtqb/loader.py`)

Reads existing `waka-data/` JSON files into Pydantic models. No API calls.

- Validates all files exist before loading
- Handles variable segment counts per day (0 to 96 observed)
- `daily_average` from `all_time.json` is in seconds — loader converts to
  human-readable form where needed

### Session Tagger (`src/mtqb/session_tagger.py`)

Writes and restores `.wakatime-project` to tag WakaTime sessions for a run,
enabling human vs agent distinction in the data.

- Tag format: `S01/cc/phase1` (sprint/agent-type/phase)
- Saves original file content before write, restores on exit (context manager)
- Works on any target repo directory

### Quality Collector (`src/mtqb/quality_collector.py`)

Runs quality tools against a target repo and returns a `QualitySnapshot`.

| Tool | Metric captured |
|------|----------------|
| `ruff check` | `lint_violations` (count) |
| `pyright` | `type_errors` (count) |
| `pytest` | `test_pass_rate` (0.0–1.0) |
| `complexipy` | `complexity_score` (aggregate) |
| `jscpd` | `duplication_pct` (0.0–100.0) |

Tools are invoked via `subprocess.run()`. Missing tools produce `None` fields,
not errors, so partial snapshots are valid.

### Correlator (`src/mtqb/correlator.py`)

Joins `WakaSummary`/`WakaSessionData` with `QualitySnapshot` by date and
session tag, then writes the output report.

- Match key: date (ISO format) + optional session tag
- Output: `results/correlation.md` (human-readable) + `results/data.csv`
  (machine-readable for further analysis)

## Pydantic Models

All models live in `src/mtqb/models.py` and use
`ConfigDict(strict=True, frozen=True)`.

### Implemented (`src/mtqb/models.py`)

```python
class SummaryProject(BaseModel):
    name: str
    total_seconds: float          # ge=0

class DailySummary(BaseModel):
    date: str
    grand_total_seconds: float    # ge=0; shape to confirm against real waka-data
    projects: list[SummaryProject]

class Project(BaseModel):
    id: str
    name: str

class AllTime(BaseModel):
    daily_average: float          # ge=0; SECONDS not minutes
    total_seconds: float          # ge=0

class DurationSegment(BaseModel):
    project: str
    duration: float               # ge=0
    time: float
```

### Planned (future modules)

```python
# src/mtqb/quality_collector.py
class QualitySnapshot(BaseModel):
    timestamp: datetime
    repo_path: str
    test_pass_rate: float | None      # 0.0–1.0
    lint_violations: int | None
    type_errors: int | None
    complexity_score: float | None
    duplication_pct: float | None     # 0.0–100.0

# src/mtqb/correlator.py
class CorrelationRecord(BaseModel):
    date: str
    session_tag: str | None
    waka_total_seconds: float
    waka_segment_count: int
    test_pass_rate: float | None
    lint_violations: int | None
    type_errors: int | None
    complexity_score: float | None
    duplication_pct: float | None
```

## Directory Structure

```
multi-tasking-quality-benchmark/
  src/
    mtqb/
      __init__.py
      models.py            # Pydantic models (implemented)
      loader.py            # waka-data/ reader → Pydantic models (stub)
      client.py            # WakaTime API client (planned)
      session_tagger.py    # .wakatime-project write/restore (planned)
      quality_collector.py # ruff + pyright + pytest + complexipy + jscpd (planned)
      correlator.py        # join + report writer (planned)
  tests/
    mtqb/
      fixtures/            # committed JSON fixtures for loader tests
      test_loader.py       # xfail TDD-red loader spec tests
  results/
    correlation.md         # generated report (gitignored)
    data.csv               # generated data (gitignored)
  docs/
    architecture.md        # this file
    UserStory.md
    TODO.md
    decisions.md
  Makefile
  Makefile.python
  pyproject.toml
  README.md
  AGENTS.md

../waka-data/              # external, shared data store (not in this repo)
```

## API Data Notes

- **Free tier**: 14-day window. `{"data": []}` outside window, no 403.
- **Duration segments**: 0–96 per day; short segments from 15-min heartbeat
  aggregation and project switches. Do not assume one segment per session.
- **`daily_average`** in `all_time.json`: stored in **seconds**, not minutes.
- **Bulk download**: omit `&project=` parameter to get all projects in one
  request; filter client-side to reduce API calls.
