"""Data contract for research findings passed between agents.

This is the single source of truth for what a "finding" looks like as it
crosses the boundary from a Researcher agent to a Writer agent. Keeping the
validation here (rather than trusting each agent to behave) means the
contract is enforced no matter which concrete agent implementation is used
on either side of the handoff.
"""

from dataclasses import dataclass


@dataclass
class ResearchFinding:
    """A single structured research finding.

    Attributes:
        claim: The factual claim or statement discovered during research.
            Must be a non-empty, non-whitespace-only string.
        source: Where the claim came from (e.g. a document name, URL, or
            fixture identifier). Must be a non-empty, non-whitespace-only
            string.
        confidence: A float in the closed interval [0.0, 1.0] representing
            how confident the researcher is in this claim.
    """

    claim: str
    source: str
    confidence: float

    def __post_init__(self) -> None:
        if not isinstance(self.claim, str) or not self.claim.strip():
            raise ValueError("ResearchFinding.claim must be a non-empty string")

        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("ResearchFinding.source must be a non-empty string")

        if isinstance(self.confidence, bool) or not isinstance(self.confidence, (int, float)):
            raise ValueError(
                f"ResearchFinding.confidence must be a number, got {type(self.confidence).__name__}"
            )

        confidence_value = float(self.confidence)
        if not (0.0 <= confidence_value <= 1.0):
            raise ValueError(
                f"ResearchFinding.confidence must be within [0.0, 1.0], got {self.confidence}"
            )
