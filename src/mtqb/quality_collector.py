"""Run quality tools against a target repo and capture a QualitySnapshot.

Each tool is looked up on PATH and run with the target repo as working
directory. A missing tool, a timeout or unparseable output yields None for
that metric instead of an error, so partial snapshots are valid.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mtqb.models import QualitySnapshot

Runner = Callable[[list[str], Path], str | None]

TOOL_TIMEOUT_SECONDS = 600
_PYTEST_COUNT = re.compile(r"(\d+) (passed|failed|errors?)\b")


def run_tool(cmd: list[str], cwd: Path) -> str | None:
    """Run cmd in cwd and return its stdout, or None if the tool is missing or hangs."""
    exe = shutil.which(cmd[0])
    if exe is None:
        return None
    try:
        # Reason: argv list (no shell); executable resolved via shutil.which.
        result = subprocess.run(  # noqa: S603
            [exe, *cmd[1:]],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=TOOL_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    return result.stdout


def _lint_violations(run: Runner, repo: Path) -> int | None:
    out = run(["ruff", "check", "--output-format=json", "--exit-zero", "--no-cache", "."], repo)
    if out is None:
        return None
    try:
        return len(json.loads(out))
    except ValueError:
        return None


def _type_errors(run: Runner, repo: Path) -> int | None:
    out = run(["pyright", "--outputjson"], repo)
    if out is None:
        return None
    try:
        return int(json.loads(out)["summary"]["errorCount"])
    except (ValueError, KeyError, TypeError):
        return None


def _test_pass_rate(run: Runner, repo: Path) -> float | None:
    out = run(["pytest", "-q", "--no-header", "-p", "no:cacheprovider"], repo)
    if out is None:
        return None
    counts = {"passed": 0, "failed": 0, "error": 0}
    for num, kind in _PYTEST_COUNT.findall(out):
        counts[kind.rstrip("s")] += int(num)
    total = sum(counts.values())
    return counts["passed"] / total if total else None


def _json_report(run: Runner, repo: Path, cmd: list[str], output: str, report: str) -> Any:
    """Run cmd with `--output <tmp>/<output>` and return the parsed JSON at <tmp>/<report>.

    Returns None if the tool is missing or the report is absent or not JSON.
    """
    with tempfile.TemporaryDirectory() as tmp:
        if run([*cmd, "--output", str(Path(tmp, output))], repo) is None:
            return None
        try:
            return json.loads(Path(tmp, report).read_text())
        except (OSError, ValueError):
            return None


def _complexity_score(run: Runner, repo: Path) -> float | None:
    """Sum of cognitive complexity over all functions in the repo."""
    # Reason: --plain text output wraps long paths at console width; the JSON report doesn't.
    cmd = ["complexipy", "--quiet", "--ignore-complexity", "--output-format", "json", "."]
    report = _json_report(run, repo, cmd, "complexipy.json", "complexipy.json")
    if report is None:
        return None
    try:
        return float(sum(fn["complexity"] for fn in report))
    except (KeyError, TypeError):
        return None


def _duplication_pct(run: Runner, repo: Path) -> float | None:
    cmd = ["jscpd", ".", "--silent", "--gitignore", "--reporters", "json"]
    report = _json_report(run, repo, cmd, "", "jscpd-report.json")
    if report is None:
        return None
    try:
        return float(report["statistics"]["total"]["percentage"])
    except (KeyError, TypeError):
        return None


def collect(repo: Path, run: Runner = run_tool) -> QualitySnapshot:
    """Run all five quality tools against repo and return the snapshot."""
    return QualitySnapshot(
        timestamp=datetime.now(UTC),
        repo_path=str(repo),
        test_pass_rate=_test_pass_rate(run, repo),
        lint_violations=_lint_violations(run, repo),
        type_errors=_type_errors(run, repo),
        complexity_score=_complexity_score(run, repo),
        duplication_pct=_duplication_pct(run, repo),
    )


def main(argv: list[str]) -> int:
    """CLI entry: print the snapshot of the repo given as the only argument as JSON."""
    if len(argv) != 1 or not Path(argv[0]).is_dir():
        print("usage: python -m mtqb.quality_collector <repo-dir>", file=sys.stderr)
        return 2
    print(collect(Path(argv[0])).model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
