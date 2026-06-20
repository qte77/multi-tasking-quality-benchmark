---
title: User Story - multi-tasking-quality-benchmark
description: User stories for correlating WakaTime coding activity with code quality metrics
category: requirements
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
---

# User Story: multi-tasking-quality-benchmark

## Problem Statement

There is no way to correlate WakaTime coding activity metrics with code quality
outcomes. Developers and researchers cannot determine whether more coding time,
different session patterns, or human vs agent contributions improve or degrade
code quality.

## Target Users

Developers and researchers analyzing coding productivity vs code quality.

## Value Proposition

Link WakaTime activity data (time, sessions, AI vs human edits) with quality
snapshots (lint, types, tests, complexity, duplication) to discover patterns
between coding effort and code quality.

## User Stories

- As a researcher, I want to poll the WakaTime API and persist data to
  `waka-data/` so that I have a local store of coding activity metrics.
- As a researcher, I want to load existing WakaTime data from `waka-data/`
  (summaries, durations, projects, all_time) so that I can analyze previously
  collected data without API calls.
- As a researcher, I want to run a quality snapshot on a codebase (ruff,
  pyright, pytest, complexipy, jscpd) so that I can capture code quality at a
  point in time.
- As a researcher, I want to correlate coding activity with quality metrics so
  that I can identify patterns between effort and quality.
- As a researcher, I want to generate a correlation report (markdown + CSV) so
  that I can share findings and visualize trends.
- As a researcher, I want to tag WakaTime sessions for agent runs so that I can
  distinguish human vs agent coding activity.

## Success Criteria

1. `make waka-poll` writes `summaries.json` and `durations/YYYY-MM-DD.json`
   files to `waka-data/`.
2. `make waka-load` reads existing `waka-data/` files into Pydantic models
   without API calls.
3. `make quality-snapshot REPO=path` produces a `QualitySnapshot` with
   lint_violations, type_errors, test_pass_rate, complexity_score, and
   duplication_pct.
4. `make waka-correlate` joins WakaTime data with quality snapshots and writes
   `results/correlation.md` + `results/data.csv`.
5. Session tagger writes `.wakatime-project` with format `S01/cc/phase1` before
   runs and restores original after.
6. Data loader handles the variable number of duration segments per day
   (0-96 observed).

## Constraints

- WakaTime free tier: 14 days of data only
- API key from `~/.wakatime.cfg` (takes precedence over `WAKATIME_API_KEY`
  env var)
- Python 3.13+
- `waka-data/` directory is the canonical data store (shared across tools)

## Research Framing

### Hypothesis

Longer or more focused coding sessions, and human-authored contributions (as
opposed to agent-generated code), correlate with measurable improvements in
code quality metrics (fewer lint violations, fewer type errors, higher test
pass rates, lower complexity).

### Interpretation

- **Positive correlation** (more time / human contribution → better quality):
  suggests sustained focus and human judgment improve code quality; informs
  decisions to invest in longer uninterrupted sessions and limit agent autonomy
  for quality-critical paths.
- **Negative correlation** (more time / human contribution → worse quality):
  may indicate fatigue effects or that agent-assisted sessions introduce
  discipline (consistent linting, typing); prompts re-evaluation of
  human-only workflows.
- **Null result**: session length or authorship type alone does not predict
  quality; directs focus to other factors (spec quality, review practices).

### Research Success Criteria

1. The correlation dataset covers at least 14 session-days with both activity
   data and quality snapshots, enabling meaningful pattern detection.
2. Results distinguish human vs agent sessions via `.wakatime-project` tags,
   not just total time.
3. The analysis produces a reproducible pipeline (committed fixtures, versioned
   code) so findings can be independently validated or extended.

## Out of Scope

- Wakapi self-hosted server setup
- WakaTime paid tier backfill automation
- Real-time monitoring or dashboards
- Statistical significance testing (exploratory analysis only)
