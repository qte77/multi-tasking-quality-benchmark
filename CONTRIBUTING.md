<!-- DERIVED — do not hand-edit the skeleton structure. Source of truth:
     https://raw.githubusercontent.com/qte77/qte77/main/docs/templates/CONTRIBUTING.template.md
     Content below is this repo's filled-in copy; re-sync structure via
     'make sync' upstream. -->

# Contributing

For agent behavioural rules see [AGENTS.md](AGENTS.md).

## Documentation hierarchy

One audience per file — reference, don't duplicate (estate contract: [doc-structure.md](https://github.com/qte77/qte77/blob/main/docs/doc-structure.md)):

| File | Audience | Owns |
| --- | --- | --- |
| [README.md](README.md) | users | what, why, how — the front door |
| CONTRIBUTING.md | contributors | workflow, commands, releasing |
| [AGENTS.md](AGENTS.md) | AI agents | behavioural rules (`CLAUDE.md` loads the same) |
| `changelog.d/*.md` | everyone | changes; released via `scriv collect` |

## Commands

```bash
make help             # list all recipes
make validate_quick   # ruff + pyright + complexipy + pytest (no coverage gate)
make validate         # same, plus the 70% coverage gate (pyproject.toml)
make test_all         # uv run pytest
make lint_md FILES="*.md"    # markdownlint --fix
make lint_links               # lychee link check
```

## Conventional Commits

`feat`, `fix`, `docs`, `chore`, `refactor`. Optional scope:
`feat(SCOPE): ...`. PR titles match.

## Branches

- `feat/TOPIC`, `fix/TOPIC`, `docs/TOPIC`, `chore/TOPIC`
- Squash-merge is default. Force-push only with `--force-with-lease`, never to `main`.

## CHANGELOG

This repo uses [scriv](https://scriv.readthedocs.io/): add a fragment under
`changelog.d/` for any consumer-visible change (see existing fragments for
format/category headers). `scriv collect` compiles fragments into
`CHANGELOG.md` at release time — there is no committed `CHANGELOG.md` yet
since no release has been cut.

## Releasing

Semi-automatic: a **human-authored** bump PR (so the merge is a real-user
event → no bot `action_required` gotcha), automatic tag, one-command
publish. SemVer; the version source of truth is `pyproject.toml`, mirrored
in the README version badge (`-blue`).

1. Release PR: `uv run bump-my-version bump PART`, update the README badge,
   and `scriv collect` to roll fragments into `CHANGELOG.md`.
2. Merge → tag `vX.Y.Z` on the version change.
3. Optionally publish a GitHub Release from the matching `CHANGELOG.md`
   block. Tag-only is fine.

## Pre-merge

1. `make validate_quick` clean
2. `make lint_md FILES="*.md"` clean
3. `make lint_links` clean
4. Conventional Commits title
