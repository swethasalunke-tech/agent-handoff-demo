# Build Schedule

## Day 1 (this commit)

- Define the `ResearchFinding` contract with real validation
  (`handoff/contract.py`).
- Implement `FakeResearcherAgent`, backed by a hand-authored fixture file
  (`data/research_fixtures.json`), and `FakeWriterAgent`, with real
  confidence-tier grouping and citation logic. Neither makes any live LLM
  call.
- Wire them together with `run_handoff()` (`handoff/pipeline.py`).
- Full pytest suite covering the contract, both fake agents, and the
  end-to-end pipeline (including error propagation for an unknown topic).
- Every test in this commit is run locally before pushing, and the actual
  `pytest` output is what's reported - no invented pass counts.

## Day 2 (planned)

- Add a real, Anthropic-backed `ResearcherAgent` implementing the same
  `research(topic) -> list[ResearchFinding]` interface as
  `FakeResearcherAgent`, following the fake/real dependency-injection
  pattern already used in this account's `weekly-ai-tutor` repo.
- `FakeResearcherAgent` stays in the codebase and continues to back the
  deterministic tests; the real agent is exercised separately (e.g. a
  manual smoke-test script or an explicitly-marked integration test that
  requires an API key and is not part of the default `pytest` run).
- Live-API caveat, stated honestly: any example output from the real
  `ResearcherAgent` shown in the README or commit message will be actual
  output captured from a real run, dated, and labeled as such - never
  invented. If no live run has been done yet, no "example output" will be
  shown for it.
- Cost/rate-limit handling for real API calls is scoped for this day too
  (timeouts, retries, and a clear error if the API key is missing).

## Day 3 (planned)

- Add a real, Anthropic-backed `WriterAgent` implementing the same
  `compose(findings) -> str` interface as `FakeWriterAgent`, same
  fake/real pattern as Day 2.
- Run the full pipeline end-to-end with the real Researcher and real
  Writer at least once, capture the actual output, and document it
  honestly (dated, labeled as a real run, not a fabricated sample).
- Revisit `DESIGN.md`'s "explicitly deferred" list and update it based on
  what's now implemented.
