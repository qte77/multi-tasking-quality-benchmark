"""Pydantic models for WakaTime API JSON shapes consumed by the loader.

All models use strict + frozen config: fields are validated on construction
and instances are immutable after creation.
"""

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
