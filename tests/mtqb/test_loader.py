"""Behavior tests for WakaLoader.

Fixtures live at tests/mtqb/fixtures/ and are committed to the repo.
"""

import shutil
from pathlib import Path

import pytest

from mtqb.loader import WakaLoader

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_projects_returns_two_projects() -> None:
    # Arrange
    loader = WakaLoader(FIXTURES)
    # Act
    projects = loader.load_projects()
    # Assert
    assert len(projects) == 2  # noqa: S101


def test_load_all_time_daily_average_is_seconds() -> None:
    # Arrange
    loader = WakaLoader(FIXTURES)
    # Act
    all_time = loader.load_all_time()
    # Assert — daily_average must be 7200 seconds (2 hours), NOT in minutes
    assert all_time.daily_average == 7200.0  # noqa: S101


def test_load_summaries_returns_two_days() -> None:
    # Arrange
    loader = WakaLoader(FIXTURES)
    # Act
    summaries = loader.load_summaries()
    # Assert
    assert len(summaries) == 2  # noqa: S101


def test_load_durations_returns_three_segments() -> None:
    # Arrange
    loader = WakaLoader(FIXTURES)
    # Act
    segments = loader.load_durations("2026-03-09")
    # Assert
    assert len(segments) == 3  # noqa: S101


def test_load_durations_missing_date_raises() -> None:
    # Arrange
    loader = WakaLoader(FIXTURES)
    # Act / Assert
    with pytest.raises(FileNotFoundError):
        loader.load_durations("1970-01-01")


def test_loader_respects_configurable_data_dir(tmp_path: Path) -> None:
    # Arrange — copy fixtures into an isolated tmp_path directory
    shutil.copytree(str(FIXTURES), str(tmp_path / "data"))
    loader = WakaLoader(tmp_path / "data")
    # Act
    projects = loader.load_projects()
    # Assert — loader reads from the supplied data_dir, not a hardcoded path
    assert len(projects) == 2  # noqa: S101


def test_load_durations_envelope_unwrapped() -> None:
    """The loader unwraps {"data": [...]} rather than returning the raw dict."""
    # Arrange
    loader = WakaLoader(FIXTURES)
    # Act
    segments = loader.load_durations("2026-03-09")
    # Assert — each item is a DurationSegment, not a raw dict
    from mtqb.models import DurationSegment

    assert all(isinstance(s, DurationSegment) for s in segments)  # noqa: S101


