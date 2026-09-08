# agent-handoff-demo

A small demo of a **validated, tested handoff between two agents**: a
Researcher agent produces structured findings, and a Writer agent consumes
them to compose a draft. The point is the contract between the agents -
not a loose "paste one agent's output into another's prompt" chain, but a
typed, validated data structure that's enforced and tested on both sides.

## Status: Day 1 - fake/fixture-based agents, no live LLM calls yet

Everything in this repo right now is **deterministic and offline**:

- `FakeResearcherAgent` reads its "findings" from a hand-authored fixture
  file (`data/research_fixtures.json`), not from any model or live
  research process.
- `FakeWriterAgent` composes its draft with real, deterministic logic
  (grouping by confidence tier, formatting citations) - also not backed by
  any model.
- No network calls, no API keys, no live verification claims are made
  anywhere in this repo. What's here is what actually runs, and it's
  covered by tests that actually pass (see below).

A real, Anthropic-backed Researcher and Writer are planned for Day 2 and
Day 3 respectively, behind the same interfaces - see `BUILD-SCHEDULE.md`
and `DESIGN.md` for the plan and what's explicitly out of scope for now.

## What's implemented

- `handoff/contract.py` - the `ResearchFinding` dataclass: `claim: str`,
  `source: str`, `confidence: float`, with real validation in
  `__post_init__` (raises `ValueError` for an empty claim, empty source,
  or a confidence outside `[0.0, 1.0]`).
- `handoff/researcher.py` - `FakeResearcherAgent.research(topic)`, which
  looks up `topic` in `data/research_fixtures.json` and returns a list of
  validated `ResearchFinding` objects, or raises `UnknownTopicError` for a
  topic that isn't in the fixture data. Fixture topics currently included:
  `http-status-codes`, `python-virtual-environments`, `git-basics`.
- `handoff/writer.py` - `FakeWriterAgent.compose(findings)`, which groups
  findings into "High confidence" (>= 0.85), "Medium confidence"
  (>= 0.6), and "Low confidence" tiers, and renders a Markdown draft
  citing each finding's source. Raises `EmptyFindingsError` on an empty
  list instead of silently producing nothing.
- `handoff/pipeline.py` - `run_handoff(topic, researcher, writer)`, which
  wires a researcher and a writer together via constructor injection and
  lets errors from either side propagate unchanged.
- `tests/` - a full pytest suite covering the contract's validation rules,
  both fake agents, and the end-to-end pipeline (including the error path
  where an unknown topic propagates all the way out of `run_handoff()`).

## Running the tests

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v
```

This repo's test suite currently has 23 tests across
`test_contract.py`, `test_researcher.py`, `test_writer.py`, and
`test_pipeline.py`, and all of them pass. Run the command above yourself
to see the live output - this README intentionally does not paste a
"sample" test run, since that's exactly the kind of claim this account
does not make without it actually happening.

## Layout

```
handoff/
  contract.py    # ResearchFinding dataclass + validation
  researcher.py  # FakeResearcherAgent
  writer.py      # FakeWriterAgent
  pipeline.py    # run_handoff() orchestration
data/
  research_fixtures.json  # hand-authored fixture findings, see file for provenance notes
tests/
  test_contract.py
  test_researcher.py
  test_writer.py
  test_pipeline.py
DESIGN.md          # scope, and what's explicitly deferred
BUILD-SCHEDULE.md  # day-by-day build plan
```
