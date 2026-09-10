# multi-tasking-quality-benchmark

> Correlate WakaTime coding activity with code quality metrics — for
> developers and researchers asking whether time, session patterns, or
> human-vs-agent authorship move code quality.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-blue.svg)](changelog.d/)
[![CodeQL](https://github.com/qte77/multi-tasking-quality-benchmark/actions/workflows/codeql.yaml/badge.svg)](https://github.com/qte77/multi-tasking-quality-benchmark/actions/workflows/codeql.yaml)

## What

- Polls the WakaTime API into an external `../waka-data/` store (summaries,
  durations, projects, all-time) — not part of this checkout
- Loads that store into strict, frozen Pydantic models; analysis needs no
  further API calls
- Snapshots a target repo's quality: lint violations, type errors, test pass
  rate, complexity, duplication
- Tags WakaTime sessions (`S01/cc/phase1`) to separate human from agent
  coding activity
- Joins activity and quality by date + session tag into
  `results/correlation.md` and `results/data.csv`
- Design, data-store layout, API notes, and the quality-tool table:
  [docs/architecture.md](docs/architecture.md); status (early, Phase 0) and
  next steps: [docs/TODO.md](docs/TODO.md)

## How

```bash
make waka-poll        # fetch latest WakaTime data → ../waka-data/
make waka-correlate   # join activity + quality snapshots → results/
```

Both targets are Phase-0 placeholders until the client and correlator land
(see [docs/TODO.md](docs/TODO.md)). Pipeline and component details:
[docs/architecture.md](docs/architecture.md).

## Why

WakaTime reports *how long* you coded; agent harnesses such as
[coding-harness-eval](https://github.com/qte77/coding-harness-eval) report *how
well* an agent scored — neither ties coding time, session patterns, or
human-vs-agent authorship to code-quality outcomes. This repo joins the two:
tagged WakaTime sessions against lint/type/test/complexity/duplication
snapshots, so the effect of effort and authorship on quality becomes
measurable. Hypotheses and framing: [docs/UserStory.md](docs/UserStory.md).

## Refs

- [CONTRIBUTING.md](CONTRIBUTING.md) — workflow, commands, releasing
- [docs/architecture.md](docs/architecture.md) — data flow, components, API
  notes
- [docs/UserStory.md](docs/UserStory.md) — problem statement and hypotheses
- [docs/decisions.md](docs/decisions.md) — ADR-lite decision log
- [docs/TODO.md](docs/TODO.md) — status and next steps
- [coding-harness-eval](https://github.com/qte77/coding-harness-eval) — agent
  evaluation harness
- [An Open Agentic Coding Harness](https://qte77.github.io/open-agentic-coding-harness/)
  — write-up
- [WakaTime API](https://wakatime.com/developers) — data source

## License

Apache-2.0 — see [LICENSE](LICENSE).
