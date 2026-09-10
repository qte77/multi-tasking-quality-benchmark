"""WakaLoader — reads waka-data/ JSON files into Pydantic models.

Expected file layout under data_dir:
    summaries.json          — {"data": [<DailySummary>, ...]}
    projects.json           — {"data": [<Project>, ...]}
    all_time.json           — flat AllTime object (no envelope)
    durations/<date>.json   — {"data": [<DurationSegment>, ...]}
"""

import json
from pathlib import Path

from mtqb.models import AllTime, DailySummary, DurationSegment, Project


class WakaLoader:
    """Reads existing waka-data/ JSON files into Pydantic models without API calls."""

    def __init__(self, data_dir: Path) -> None:
        """Initialise the loader.

        Args:
            data_dir: Path to the waka-data directory (may be absolute or relative).
                      All file lookups are relative to this directory.
        """
        self._data_dir = data_dir

    def load_summaries(self) -> list[DailySummary]:
        """Load daily coding summaries from summaries.json.

        Unwraps the {"data": [...]} envelope and validates each entry as a
        DailySummary. Returns entries in the order they appear in the file.

        Returns:
            List of DailySummary objects, one per recorded day.

        Raises:
            FileNotFoundError: if summaries.json does not exist under data_dir.
        """
        entries = self._read_envelope("summaries.json")
        return [DailySummary.model_validate(entry) for entry in entries]

    def load_projects(self) -> list[Project]:
        """Load the project list from projects.json.

        Unwraps the {"data": [...]} envelope and validates each entry as a
        Project.

        Returns:
            List of Project objects.

        Raises:
            FileNotFoundError: if projects.json does not exist under data_dir.
        """
        entries = self._read_envelope("projects.json")
        return [Project.model_validate(entry) for entry in entries]

    def load_all_time(self) -> AllTime:
        """Load lifetime totals from all_time.json.

        The file is a flat JSON object (no "data" envelope). daily_average is
        stored in seconds, not minutes.

        Returns:
            An AllTime model with daily_average (seconds) and total_seconds.

        Raises:
            FileNotFoundError: if all_time.json does not exist under data_dir.
        """
        path = self._data_dir / "all_time.json"
        data = json.loads(path.read_text())
        return AllTime.model_validate(data)

    def load_durations(self, date: str) -> list[DurationSegment]:
        """Load duration segments for a specific date from durations/<date>.json.

        Unwraps the {"data": [...]} envelope and validates each entry as a
        DurationSegment. The number of segments per day varies from 0 to 96
        (15-minute heartbeat aggregation + project switches).

        Args:
            date: ISO date string, e.g. "2026-03-09". Maps to
                  data_dir/durations/<date>.json.

        Returns:
            List of DurationSegment objects for that date (may be empty).

        Raises:
            FileNotFoundError: if durations/<date>.json does not exist under data_dir.
        """
        entries = self._read_envelope(f"durations/{date}.json")
        return [DurationSegment.model_validate(entry) for entry in entries]

    def _read_envelope(self, relative_path: str) -> list[dict[str, object]]:
        """Read a JSON file under data_dir and unwrap its {"data": [...]} envelope.

        Args:
            relative_path: Path relative to data_dir, e.g. "projects.json" or
                            "durations/2026-03-09.json".

        Returns:
            The list of raw entries under the "data" key.

        Raises:
            FileNotFoundError: if the file does not exist under data_dir.
        """
        path = self._data_dir / relative_path
        payload = json.loads(path.read_text())
        return payload["data"]
