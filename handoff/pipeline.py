"""Orchestration wiring a Researcher agent to a Writer agent.

run_handoff() is intentionally small: it exists to demonstrate that the
Researcher and Writer can be wired together through the ResearchFinding
contract, and that errors from either side propagate honestly instead of
being caught and hidden.
"""

from typing import List, Protocol

from .contract import ResearchFinding


class Researcher(Protocol):
    def research(self, topic: str) -> List[ResearchFinding]: ...


class Writer(Protocol):
    def compose(self, findings: List[ResearchFinding]) -> str: ...


def run_handoff(topic: str, researcher: Researcher, writer: Writer) -> str:
    """Run the Researcher -> Writer handoff for a given topic.

    Args:
        topic: the topic to research and write about.
        researcher: any object implementing research(topic) -> list[ResearchFinding].
        writer: any object implementing compose(findings) -> str.

    Returns:
        The composed draft string produced by the writer.

    Raises:
        Whatever researcher.research() or writer.compose() raise. Errors
        are deliberately NOT caught or swallowed here - a broken research
        step should never silently produce an empty or misleading draft.
    """
    findings = researcher.research(topic)
    return writer.compose(findings)
