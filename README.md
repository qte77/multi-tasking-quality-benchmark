# multi-tasking-quality-benchmark

Correlate WakaTime coding activity with code quality metrics.

## What

Consumes WakaTime API data from `../waka-data/`, runs quality tools against
target codebases, and joins activity data with quality snapshots by session tag.
This enables analysis of whether more coding time, different session patterns,
or human vs agent contributions correlate with better or worse code quality.

## Data Source

`../waka-data/` — an external data store, **not present in this checkout**.
Fetch it with `make waka-poll`. Tests run against committed fixtures under
`tests/mtqb/fixtures/`.

```
waka-data/
  summaries.json          # aggregated coding stats per day
  projects.json           # project list
  all_time.json           # lifetime totals (daily_average in seconds, not minutes)
  durations/
    2026-03-09.json       # daily duration segments
    ...
    YYYY-MM-DD.json
```

This repo reads from that directory. It does not own or manage it.

## Quick Start

```bash
make waka-poll        # fetch latest WakaTime data → waka-data/
make waka-correlate   # join activity + quality snapshots → results/
```

## WakaTime API Notes

- **Auth**: HTTP Basic, API key as username, empty password: `base64(key:)`
- **Key source**: `~/.wakatime.cfg` (`api_key=` field) — takes precedence over
  `WAKATIME_API_KEY` env var
- **Free tier**: 14 days of history only. Outside the window returns
  `{"data": []}` (no 403). Paid tier ($11.99/mo) unlocks full history on the
  same endpoints.
- **Bulk download**: omit `&project=` param to get all projects in one call,
  filter client-side
- **`all_time_since_today`**: undocumented endpoint, returns lifetime total;
  `daily_average` field is in **seconds**, not minutes

## Key Data Facts

- Duration segments per day vary from 0 to 96 (short segments, not one per session)
- 15-minute heartbeat aggregation + project switches produce many short segments
- Session correlation uses `.wakatime-project` file tag, not time-window alignment

## Quality Tools

| Tool | Measures |
|------|----------|
| ruff | Lint violations |
| pyright | Type errors |
| pytest | Test pass rate |
| complexipy | Cyclomatic complexity score |
| jscpd | Code duplication percentage |

## Status

**Phase 0** — scaffold complete; loader logic pending.

- [x] Foundational documentation (README, UserStory, architecture, TODO, decisions)
- [x] Repo scaffold to estate standard (pyproject.toml, Makefile, .editorconfig,
      ruff/pyright/complexipy/pytest/scriv, .claude/rules/, AGENTS.md)
- [x] Pydantic models defined (`src/mtqb/models.py`: SummaryProject, DailySummary,
      Project, AllTime, DurationSegment)
- [x] WakaLoader interface stubbed (`src/mtqb/loader.py`: typed stubs, NotImplementedError)
- [x] Loader spec tests added (`tests/mtqb/test_loader.py`: 7 xfail TDD-red + 1 sanity)
- [ ] WakaTime data collection (`waka-data/` — external, fetch via `make waka-poll`)
- [ ] WakaLoader logic implemented (turn RED tests GREEN)
- [ ] Quality collector
- [ ] Correlator and reporting

## Related Repos

- [coding-agent-eval](../coding-agent-eval/) — agent evaluation harness
- [cc-recursive-team-mode](../cc-recursive-team-mode/) — Claude Code recursive benchmark
- [coding-agents-research](../coding-agents-research/) — research notes and landscape

## License

MIT
