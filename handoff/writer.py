"""Fake writer agent that composes a structured draft from research findings.

This agent does NOT call any live LLM. It performs real, deterministic
composition logic - grouping findings into confidence tiers and formatting
a Markdown draft with citations back to each finding's source - so the
Researcher -> Writer contract can be exercised and tested end-to-end
without any network calls.
"""

from typing import Dict, List

from .contract import ResearchFinding

# Findings at or above this confidence are grouped into the "High
# confidence" tier of the draft.
HIGH_CONFIDENCE_THRESHOLD = 0.85

# Findings at or above this confidence (and below HIGH_CONFIDENCE_THRESHOLD)
# are grouped into the "Medium confidence" tier. Anything below this falls
# into "Low confidence".
MEDIUM_CONFIDENCE_THRESHOLD = 0.6

_TIER_ORDER = ("High confidence", "Medium confidence", "Low confidence")


class EmptyFindingsError(ValueError):
    """Raised when compose() is called with no findings to work with."""


def _confidence_tier(confidence: float) -> str:
    if confidence >= HIGH_CONFIDENCE_THRESHOLD:
        return "High confidence"
    if confidence >= MEDIUM_CONFIDENCE_THRESHOLD:
        return "Medium confidence"
    return "Low confidence"


class FakeWriterAgent:
    """A deterministic stand-in for a real writing agent.

    Groups findings into confidence tiers and renders a structured Markdown
    draft, citing each finding's source and confidence score. Intended for
    Day 1 of agent-handoff-demo. A real, Anthropic-backed WriterAgent
    behind the same interface is planned for a later day (see
    BUILD-SCHEDULE.md).
    """

    def compose(self, findings: List[ResearchFinding]) -> str:
        """Compose a Markdown draft grouped by confidence tier.

        Raises:
            EmptyFindingsError: if findings is empty. Composing a draft
                from zero findings would silently produce a misleading
                "empty but valid-looking" document, so this is treated as
                an error rather than being allowed to pass through.
        """
        if not findings:
            raise EmptyFindingsError(
                "FakeWriterAgent.compose() requires at least one ResearchFinding"
            )

        tiers: Dict[str, List[ResearchFinding]] = {name: [] for name in _TIER_ORDER}
        for finding in findings:
            tiers[_confidence_tier(finding.confidence)].append(finding)

        lines: List[str] = ["# Draft", ""]
        for tier_name in _TIER_ORDER:
            tier_findings = tiers[tier_name]
            if not tier_findings:
                continue
            lines.append(f"## {tier_name}")
            lines.append("")
            for finding in tier_findings:
                lines.append(
                    f"- {finding.claim} (source: {finding.source}, "
                    f"confidence: {finding.confidence:.2f})"
                )
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"
