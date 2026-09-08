import pytest

from handoff.contract import ResearchFinding
from handoff.writer import FakeWriterAgent, EmptyFindingsError


def test_compose_rejects_empty_list():
    writer = FakeWriterAgent()
    with pytest.raises(EmptyFindingsError):
        writer.compose([])


def test_compose_includes_all_claims_and_sources():
    writer = FakeWriterAgent()
    findings = [
        ResearchFinding(claim="Claim A", source="Source A", confidence=0.9),
        ResearchFinding(claim="Claim B", source="Source B", confidence=0.5),
    ]
    draft = writer.compose(findings)
    assert "Claim A" in draft
    assert "Source A" in draft
    assert "Claim B" in draft
    assert "Source B" in draft


def test_compose_groups_findings_by_confidence_tier_in_order():
    writer = FakeWriterAgent()
    findings = [
        ResearchFinding(claim="High claim", source="S1", confidence=0.95),
        ResearchFinding(claim="Medium claim", source="S2", confidence=0.7),
        ResearchFinding(claim="Low claim", source="S3", confidence=0.2),
    ]
    draft = writer.compose(findings)

    high_idx = draft.index("High confidence")
    medium_idx = draft.index("Medium confidence")
    low_idx = draft.index("Low confidence")
    assert high_idx < medium_idx < low_idx

    high_claim_idx = draft.index("High claim")
    medium_claim_idx = draft.index("Medium claim")
    low_claim_idx = draft.index("Low claim")
    assert high_idx < high_claim_idx < medium_idx
    assert medium_idx < medium_claim_idx < low_idx
    assert low_idx < low_claim_idx


def test_compose_places_boundary_confidence_in_correct_tier():
    writer = FakeWriterAgent()
    findings = [
        ResearchFinding(claim="Exactly high", source="S1", confidence=0.85),
        ResearchFinding(claim="Exactly medium", source="S2", confidence=0.6),
        ResearchFinding(claim="Just below medium", source="S3", confidence=0.59),
    ]
    draft = writer.compose(findings)
    high_section = draft.split("## Medium confidence")[0]
    assert "Exactly high" in high_section

    medium_section = draft.split("## Medium confidence")[1].split("## Low confidence")[0]
    assert "Exactly medium" in medium_section

    low_section = draft.split("## Low confidence")[1]
    assert "Just below medium" in low_section


def test_compose_omits_empty_tiers():
    writer = FakeWriterAgent()
    findings = [ResearchFinding(claim="Only claim", source="S1", confidence=0.95)]
    draft = writer.compose(findings)
    assert "Medium confidence" not in draft
    assert "Low confidence" not in draft
    assert "High confidence" in draft
