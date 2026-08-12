# Guard v0.0.1

Initial public research release of Safety-Guard Dynamics.

## Included

- Unified research report in PDF and generated HTML editions.
- FAccT-targeted anonymous manuscript PDF.
- Research and executive presentation decks.
- Ledger-gated benchmark explorer containing the approved `v1_hmda2022` public test release.
- Reproducibility tooling, study registry, distribution ledger, and verification workflows.

## Evidence boundary

This release preserves the repository’s study-level evidence tiers. Acts I–II are retrospective
fixed-panel analyses; the mortgage labels are LLM-judge and policy-card-consistent rather than
SME-adjudicated; the stopped Paper C line authorizes no claim. The Paper C successor’s stale
candidate-lock check remains a declared expected failure and is not presented as release evidence.

## Verification

The release was checked with the root tests, publication and distribution gates, registry/index/link
validation, Mortgage benchmark tests, Paper B tests, and the historical Paper C predecessor suite.
GitHub Actions verify runs on Python 3.12; Pages publication remains an explicit workflow dispatch
behind the source distribution gate.

## Licensing and distribution

Source-level redistribution decisions live in `benchmarks/registry/distribution.yaml`. Only the
affirmatively approved `v1_hmda2022` source is emitted with text by the public explorer; other
sources remain text-free or local-only.
