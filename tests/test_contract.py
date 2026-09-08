import pytest

from handoff.contract import ResearchFinding


def test_valid_finding_is_constructed():
    finding = ResearchFinding(
        claim="Water boils at 100 degrees Celsius at sea level.",
        source="Physics reference",
        confidence=0.9,
    )
    assert finding.claim == "Water boils at 100 degrees Celsius at sea level."
    assert finding.source == "Physics reference"
    assert finding.confidence == 0.9


def test_empty_claim_raises_value_error():
    with pytest.raises(ValueError, match="claim"):
        ResearchFinding(claim="", source="Some source", confidence=0.5)


def test_whitespace_only_claim_raises_value_error():
    with pytest.raises(ValueError, match="claim"):
        ResearchFinding(claim="   ", source="Some source", confidence=0.5)


def test_empty_source_raises_value_error():
    with pytest.raises(ValueError, match="source"):
        ResearchFinding(claim="A claim", source="", confidence=0.5)


def test_whitespace_only_source_raises_value_error():
    with pytest.raises(ValueError, match="source"):
        ResearchFinding(claim="A claim", source="   ", confidence=0.5)


def test_confidence_below_zero_raises_value_error():
    with pytest.raises(ValueError, match="confidence"):
        ResearchFinding(claim="A claim", source="A source", confidence=-0.01)


def test_confidence_above_one_raises_value_error():
    with pytest.raises(ValueError, match="confidence"):
        ResearchFinding(claim="A claim", source="A source", confidence=1.01)


def test_non_numeric_confidence_raises_value_error():
    with pytest.raises(ValueError, match="confidence"):
        ResearchFinding(claim="A claim", source="A source", confidence="high")


def test_confidence_boundary_values_are_valid():
    low = ResearchFinding(claim="A claim", source="A source", confidence=0.0)
    high = ResearchFinding(claim="A claim", source="A source", confidence=1.0)
    assert low.confidence == 0.0
    assert high.confidence == 1.0
