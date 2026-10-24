"""Behavior tests for the quality collector.

Tool invocations are replaced by a fake runner returning canned tool output,
so tests never depend on which quality tools are installed.
"""

import json
import sys
from pathlib import Path

from mtqb.quality_collector import collect, run_tool

RUFF_OUT = json.dumps([{"code": "E501"}, {"code": "F401"}, {"code": "S101"}])
PYRIGHT_OUT = json.dumps({"summary": {"errorCount": 2, "warningCount": 5}})
PYTEST_OUT = "...F\n3 passed, 1 failed, 2 skipped in 0.12s\n"
COMPLEXIPY_REPORT = [{"complexity": 4}, {"complexity": 0}, {"complexity": 7}]
JSCPD_REPORT = {"statistics": {"total": {"percentage": 12.5}}}


def _fake_runner(outputs: dict[str, str | None]):
    """Return a runner that answers each tool by name.

    jscpd and complexipy report via a file at --output (jscpd: a directory),
    so for them the canned output is written there instead of returned.
    """

    def run(cmd: list[str], cwd: Path) -> str | None:
        out = outputs.get(cmd[0])
        if "--output" not in cmd or out is None:
            return out
        target = Path(cmd[cmd.index("--output") + 1])
        report = target / "jscpd-report.json" if cmd[0] == "jscpd" else target
        report.write_text(out)
        return ""

    return run


ALL_TOOLS: dict[str, str | None] = {
    "ruff": RUFF_OUT,
    "pyright": PYRIGHT_OUT,
    "pytest": PYTEST_OUT,
    "complexipy": json.dumps(COMPLEXIPY_REPORT),
    "jscpd": json.dumps(JSCPD_REPORT),
}


def test_collect_parses_all_five_metrics(tmp_path: Path) -> None:
    # Act
    snap = collect(tmp_path, run=_fake_runner(ALL_TOOLS))
    # Assert
    assert snap.repo_path == str(tmp_path)  # noqa: S101
    assert snap.lint_violations == 3  # noqa: S101
    assert snap.type_errors == 2  # noqa: S101
    assert snap.test_pass_rate == 0.75  # noqa: S101 — skipped tests excluded
    assert snap.complexity_score == 11.0  # noqa: S101
    assert snap.duplication_pct == 12.5  # noqa: S101


def test_collect_missing_tools_yield_none_fields(tmp_path: Path) -> None:
    # Act
    snap = collect(tmp_path, run=_fake_runner({}))
    # Assert — a partial (here: empty) snapshot is valid, not an error
    assert snap.repo_path == str(tmp_path)  # noqa: S101
    assert snap.lint_violations is None  # noqa: S101
    assert snap.type_errors is None  # noqa: S101
    assert snap.test_pass_rate is None  # noqa: S101
    assert snap.complexity_score is None  # noqa: S101
    assert snap.duplication_pct is None  # noqa: S101


def test_collect_unparseable_output_yields_none_for_that_tool_only(tmp_path: Path) -> None:
    # Arrange
    outputs = {**ALL_TOOLS, "ruff": "error: something broke", "complexipy": "boom"}
    # Act
    snap = collect(tmp_path, run=_fake_runner(outputs))
    # Assert
    assert snap.lint_violations is None  # noqa: S101
    assert snap.complexity_score is None  # noqa: S101
    assert snap.type_errors == 2  # noqa: S101


def test_collect_no_tests_collected_gives_none_pass_rate(tmp_path: Path) -> None:
    # Arrange
    outputs = {**ALL_TOOLS, "pytest": "no tests ran in 0.01s\n"}
    # Act
    snap = collect(tmp_path, run=_fake_runner(outputs))
    # Assert — 0/0 is not a pass rate
    assert snap.test_pass_rate is None  # noqa: S101


def test_collect_pytest_errors_count_as_not_passed(tmp_path: Path) -> None:
    # Arrange
    outputs = {**ALL_TOOLS, "pytest": "1 passed, 1 error in 0.05s\n"}
    # Act
    snap = collect(tmp_path, run=_fake_runner(outputs))
    # Assert
    assert snap.test_pass_rate == 0.5  # noqa: S101


def test_run_tool_missing_executable_returns_none(tmp_path: Path) -> None:
    # Act / Assert
    assert run_tool(["mtqb-no-such-tool-xyz"], tmp_path) is None  # noqa: S101


def test_run_tool_returns_stdout_and_runs_in_repo(tmp_path: Path) -> None:
    # Act
    out = run_tool([sys.executable, "-c", "import os; print(os.getcwd())"], tmp_path)
    # Assert
    assert out is not None  # noqa: S101
    assert Path(out.strip()).resolve() == tmp_path.resolve()  # noqa: S101
