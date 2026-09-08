import pytest

from handoff.contract import ResearchFinding
from handoff.researcher import FakeResearcherAgent, UnknownTopicError


def test_known_topic_returns_expected_finding_count():
    agent = FakeResearcherAgent()
    findings = agent.research("http-status-codes")
    assert len(findings) == 4
    assert all(isinstance(f, ResearchFinding) for f in findings)


def test_all_fixture_topics_return_findings_within_expected_range():
    agent = FakeResearcherAgent()
    for topic in agent.available_topics():
        findings = agent.research(topic)
        assert 3 <= len(findings) <= 5
        assert all(isinstance(f, ResearchFinding) for f in findings)


def test_unknown_topic_raises_unknown_topic_error():
    agent = FakeResearcherAgent()
    with pytest.raises(UnknownTopicError):
        agent.research("this-topic-does-not-exist")


def test_unknown_topic_error_message_lists_available_topics():
    agent = FakeResearcherAgent()
    with pytest.raises(UnknownTopicError, match="http-status-codes"):
        agent.research("nonexistent")


def test_available_topics_includes_expected_fixtures():
    agent = FakeResearcherAgent()
    topics = agent.available_topics()
    assert "http-status-codes" in topics
    assert "python-virtual-environments" in topics
    assert "git-basics" in topics
    # "_meta" is fixture metadata, not a real topic, and must be excluded.
    assert "_meta" not in topics


def test_findings_carry_real_source_citations():
    agent = FakeResearcherAgent()
    findings = agent.research("git-basics")
    for finding in findings:
        assert finding.source.strip() != ""
        assert finding.claim.strip() != ""
