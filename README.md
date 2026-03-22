# multi-tasking-quality-benchmark

Correlate WakaTime coding activity with code quality metrics.

## What

Consumes WakaTime API data from `../waka-data/`, runs quality tools against
target codebases, and joins activity data with quality snapshots by session tag.
This enables analysis of whether more coding time, different session patterns,
or human vs agent contributions correlate with better or worse code quality.

## Data Source

`../waka-data/` — a shared local data store written by the WakaTime poll command.

Already contains 14 days of real data:

```
waka-data/
  summaries.json          # aggregated coding stats per day
  projects.json           # project list
  all_time.json           # lifetime totals (daily_average in seconds, not minutes)
  durations/
    2026-03-09.json       # daily duration segments
    ...
    2026-03-22.json
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

**Phase 0** — documentation and data collection complete.

- [x] WakaTime data collection (`waka-data/`, 14 days of real data)
- [x] Foundational documentation
- [ ] Pydantic models and data loader
- [ ] Quality collector
- [ ] Correlator and reporting

## Related Repos

- [coding-agent-eval](../coding-agent-eval/) — agent evaluation harness
- [cc-recursive-team-mode](../cc-recursive-team-mode/) — Claude Code recursive benchmark
- [coding-agents-research](../coding-agents-research/) — research notes and landscape

## License

MIT
