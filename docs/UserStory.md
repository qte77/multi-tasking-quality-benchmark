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

## Out of Scope

- Wakapi self-hosted server setup
- WakaTime paid tier backfill automation
- Real-time monitoring or dashboards
- Statistical significance testing (exploratory analysis only)
