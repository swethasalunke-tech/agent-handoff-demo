"""Fake researcher agent that reads from a bundled fixture dataset.

This agent does NOT call any live LLM and does NOT perform real-time
research. It exists to exercise the Researcher -> Writer contract
deterministically for testing and demonstration purposes. See
data/research_fixtures.json for the underlying fixture data and its
provenance notes.
"""

import json
from pathlib import Path
from typing import List, Optional

from .contract import ResearchFinding

_DEFAULT_FIXTURES_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "research_fixtures.json"
)


class UnknownTopicError(ValueError):
    """Raised when the requested topic is not present in the fixture data."""


class FakeResearcherAgent:
    """A deterministic stand-in for a real research agent.

    Reads pre-authored findings from a JSON fixture file and returns them
    as validated ResearchFinding objects. Intended for Day 1 of
    agent-handoff-demo, where the goal is to validate the contract between
    agents rather than perform live research. A real, Anthropic-backed
    ResearcherAgent behind the same interface is planned for a later day
    (see BUILD-SCHEDULE.md).
    """

    def __init__(self, fixtures_path: Optional[Path] = None):
        self._fixtures_path = Path(fixtures_path) if fixtures_path else _DEFAULT_FIXTURES_PATH
        with open(self._fixtures_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # "_meta" is descriptive metadata about the fixture file, not a topic.
        self._topics = {key: value for key, value in data.items() if not key.startswith("_")}

    def available_topics(self) -> List[str]:
        """Return the sorted list of topics present in the fixture data."""
        return sorted(self._topics.keys())

    def research(self, topic: str) -> List[ResearchFinding]:
        """Return validated findings for a topic found in the fixture data.

        Raises:
            UnknownTopicError: if the topic is not present in the fixture
                dataset. The error message lists the available topics.
        """
        if topic not in self._topics:
            raise UnknownTopicError(
                f"Unknown topic '{topic}'. Available fixture topics: {self.available_topics()}"
            )

        raw_findings = self._topics[topic]
        return [
            ResearchFinding(
                claim=item["claim"],
                source=item["source"],
                confidence=item["confidence"],
            )
            for item in raw_findings
        ]
