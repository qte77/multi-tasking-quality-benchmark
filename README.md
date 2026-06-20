# multi-tasking-quality-benchmark

Correlate WakaTime coding activity with code quality metrics.

**Write-up:** a quality benchmark in an open agentic coding harness — [An Open Agentic Coding Harness](https://qte77.github.io/open-agentic-coding-harness/).

## What

Consumes WakaTime API data from `../waka-data/`, runs quality tools against
target codebases, and joins activity data with quality snapshots by session tag.
This enables analysis of whether more coding time, different session patterns,
or human vs agent contributions correlate with better or worse code quality.

## Data Source

`../waka-data/` — an external data store, **not present in this checkout**.
Fetch it with `make waka-poll`. Tests run against committed fixtures under
`tests/mtqb/fixtures/`.

This repo reads from that directory. It does not own or manage it.

See [docs/architecture.md](docs/architecture.md) for WakaTime Client and API Data Notes.

## Quick Start

```bash
make waka-poll        # fetch latest WakaTime data → waka-data/
make waka-correlate   # join activity + quality snapshots → results/
```

## Quality Tools

Five tools: ruff, pyright, pytest, complexipy, jscpd. See [docs/architecture.md](docs/architecture.md) for details.

## Status

Phase 0 complete (scaffold, models, loader stub, spec tests). See [docs/TODO.md](docs/TODO.md) for next steps.

## Related Repos

- [coding-agent-eval](../coding-agent-eval/) — agent evaluation harness

## License

Apache-2.0
