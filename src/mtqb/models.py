"""Pydantic models for WakaTime API JSON shapes and quality snapshots.

All models use strict + frozen config: fields are validated on construction
and instances are immutable after creation.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SummaryProject(BaseModel):
    """A single project entry inside a daily summary."""

    model_config = ConfigDict(strict=True, frozen=True)

    name: str
    total_seconds: float = Field(ge=0)


class DailySummary(BaseModel):
    """One day's aggregated coding stats from summaries.json.

    Shape to confirm against real waka-data: the top-level envelope is
    {"data": [<DailySummary>, ...]}.  grand_total_seconds is the day total.
    """

    model_config = ConfigDict(strict=True, frozen=True)

    date: str
    grand_total_seconds: float = Field(ge=0)  # shape to confirm against real waka-data
    projects: list[SummaryProject]


class Project(BaseModel):
    """A project entry from projects.json."""

    model_config = ConfigDict(strict=True, frozen=True)

    id: str
    name: str


class AllTime(BaseModel):
    """Lifetime totals from all_time.json.

    Note: daily_average is in SECONDS, not minutes (WakaTime API quirk).
    """

    model_config = ConfigDict(strict=True, frozen=True)

    daily_average: float = Field(ge=0)  # SECONDS not minutes
    total_seconds: float = Field(ge=0)


class DurationSegment(BaseModel):
    """A single duration segment from durations/<date>.json.

    The JSON envelope is {"data": [<DurationSegment>, ...]}.
    """

    model_config = ConfigDict(strict=True, frozen=True)

    project: str
    duration: float = Field(ge=0)
    time: float


class QualitySnapshot(BaseModel):
    """Code quality of a target repo at one point in time.

    A metric is None when its tool is missing or its output can't be parsed;
    partial snapshots are valid (see docs/decisions.md ADR-3).
    """

    model_config = ConfigDict(strict=True, frozen=True)

    timestamp: datetime
    repo_path: str
    test_pass_rate: float | None = Field(ge=0, le=1)
    lint_violations: int | None = Field(ge=0)
    type_errors: int | None = Field(ge=0)
    complexity_score: float | None = Field(ge=0)
    duplication_pct: float | None = Field(ge=0, le=100)
