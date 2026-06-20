---
title: Decisions - multi-tasking-quality-benchmark
description: ADR-lite decision log for key design choices
category: decisions
created: 2026-06-20
updated: 2026-06-20
version: 1.0.0
---

# Decisions: multi-tasking-quality-benchmark

Short ADR-lite entries. Each entry: Context / Decision / Why.

---

## ADR-1: Session correlation via `.wakatime-project` tag, not time-window alignment

**Context:** WakaTime duration segments are short (0–96 per day, 15-min
heartbeat granularity). Correlating by time window is ambiguous when sessions
overlap or are interrupted.

**Decision:** Tag sessions via the `.wakatime-project` file with a structured
label (`S01/cc/phase1`) before a run; restore it after. The tag appears in
duration segment data, enabling exact session-to-quality-snapshot joins.

**Why:** Tag-based joins are deterministic and survive any time-window ambiguity.
The tagger is a context manager, so the original file is always restored even
if the run fails.

---

## ADR-2: External `waka-data/` store, not in-repo

**Context:** WakaTime data is personal, continuously updated, and exceeds
what belongs in a code repo. The free tier only retains 14 days.

**Decision:** `waka-data/` lives at `../waka-data/` relative to this repo,
fetched via `make waka-poll`. It is gitignored. Tests run against committed
fixtures under `tests/mtqb/fixtures/`.

**Why:** Keeps the repo lightweight and avoids leaking personal coding data.
Fixtures provide reproducible test coverage without real data.

---

## ADR-3: Five quality tools (ruff / pyright / pytest / complexipy / jscpd)

**Context:** Need a quality snapshot at a point in time covering lint, types,
test health, complexity, and duplication.

**Decision:** Run ruff (lint violations), pyright (type errors), pytest (test
pass rate), complexipy (cyclomatic complexity), jscpd (duplication percentage).
Missing tools produce `None` fields, not errors.

**Why:** These five cover the key quality dimensions without overlap. All are
already in the estate dev stack. `None` on missing tools allows partial
snapshots on repos that don't use all tools.

---

## ADR-4: Fixtures-first testing (real data absent)

**Context:** `waka-data/` is not present in this checkout. Loader logic
cannot be tested against real data in CI.

**Decision:** Commit minimal fixture JSON files under `tests/mtqb/fixtures/`
(two projects, two summary days, one durations date, all_time). Loader tests
point `WakaLoader` at `Path(__file__).parent / "fixtures"`.

**Why:** Enables deterministic, CI-safe tests with no external dependencies.
Real-data validation is deferred to `make waka-poll` + manual verification.

---

## ADR-5: MIT license

**Context:** This repo is a personal research tool under the qte77 estate.

**Decision:** MIT license, copyright 2026.

**Why:** Permissive license consistent with the exploratory, open nature of
the research. Sibling repo coding-agent-eval uses Apache-2.0; this repo's
simpler scope warrants the lighter MIT.
