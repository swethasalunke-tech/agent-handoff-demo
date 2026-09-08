import pytest

from handoff.pipeline import run_handoff
from handoff.researcher import FakeResearcherAgent, UnknownTopicError
from handoff.writer import FakeWriterAgent


def test_pipeline_end_to_end_known_topic_produces_nonempty_draft():
    researcher = FakeResearcherAgent()
    writer = FakeWriterAgent()
    draft = run_handoff("git-basics", researcher, writer)
    assert isinstance(draft, str)
    assert len(draft.strip()) > 0
    assert "# Draft" in draft


def test_pipeline_output_reflects_actual_findings():
    researcher = FakeResearcherAgent()
    writer = FakeWriterAgent()
    draft = run_handoff("python-virtual-environments", researcher, writer)
    findings = researcher.research("python-virtual-environments")
    for finding in findings:
        assert finding.claim in draft
        assert finding.source in draft


def test_pipeline_propagates_researcher_error_for_unknown_topic():
    researcher = FakeResearcherAgent()
    writer = FakeWriterAgent()
    with pytest.raises(UnknownTopicError):
        run_handoff("nonexistent-topic", researcher, writer)
