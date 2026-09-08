# Design

## What this demo is about

Multi-agent "prompt chains" (agent A's output gets pasted into agent B's
prompt) are easy to build and easy to trust too much: there's no guarantee
that what agent A produced is actually what agent B expects. This repo
demonstrates a different pattern - a **validated data contract** between a
Researcher agent and a Writer agent, where:

- The Researcher must return a list of `ResearchFinding` objects, and each
  one is validated (non-empty claim, non-empty source, confidence in
  `[0.0, 1.0]`) the moment it's constructed. Bad data cannot silently pass
  through.
- The Writer only accepts that same validated type as input, and rejects
  an empty list rather than composing a blank or misleading draft.
- The two agents are swapped in via plain constructor injection
  (`run_handoff(topic, researcher, writer)`), so any object implementing
  `research(topic) -> list[ResearchFinding]` / `compose(findings) -> str`
  can be used on either side.

## Day 1 scope (this commit)

- `handoff/contract.py`: the `ResearchFinding` dataclass and its
  validation.
- `handoff/researcher.py`: `FakeResearcherAgent`, which reads from a
  hand-authored fixture file (`data/research_fixtures.json`) instead of
  calling any live model. This lets the contract and the pipeline wiring
  be tested deterministically, with zero network calls and zero cost.
- `handoff/writer.py`: `FakeWriterAgent`, which does real (if simple)
  composition logic - grouping findings into confidence tiers and
  rendering a Markdown draft with citations - rather than a live model
  call.
- `handoff/pipeline.py`: `run_handoff()`, which wires a researcher and a
  writer together and lets errors from either side propagate unchanged.
- A full test suite (`tests/`) covering the contract's validation rules,
  both fake agents, and the end-to-end pipeline, including the error path
  where an unknown topic propagates all the way out of `run_handoff()`.

The goal of Day 1 is specifically to get the *contract* right and proven
under test, before any real model is involved. Everything downstream
(Day 2, Day 3) plugs into this same contract.

## Explicitly deferred (not in this commit)

- **Real, Anthropic-backed Researcher and Writer agents.** Day 1 uses only
  fixture-backed fakes. A live `ResearcherAgent` (and later a live
  `WriterAgent`) will be added behind the *same* interface via dependency
  injection, following the same pattern already used in this account's
  `weekly-ai-tutor` repo (fake/local implementation for tests, real
  API-backed implementation for actual use, swappable at the call site).
  See `BUILD-SCHEDULE.md` for the planned days.
- **More than two agents in the chain.** This demo intentionally stays at
  Researcher -> Writer. A longer chain (e.g. adding a Fact-Checker or
  Editor agent) is a possible future extension, not part of this demo.
- **Async or parallel handoffs.** `run_handoff()` is synchronous and
  sequential on purpose, to keep the contract itself the focus. Concurrent
  or streaming handoffs are out of scope here.

## Non-goals

This is not a production content pipeline and does not claim to produce
polished, publishable writing. It is a demonstration of how to make an
agent-to-agent handoff testable and trustworthy.
