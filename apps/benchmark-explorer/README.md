# Benchmark explorer (Phase 3 application package)

Ledger-driven build. The predecessor at [`../../benchmark-explorer/`](../../benchmark-explorer/)
is retained only as a documented compatibility surface; its bulk HTML artifact and generator
are withdrawn and must not be published.

```
src/         build.py (ledger-driven) + generate_legacy.py (copied predecessor, unmodified)
fixtures/    three synthetic rows for CI; not a benchmark reproduction
tests/       negative tests proving unlicensed text cannot reach a public build
dist/        ignored build root — public/ is audited staging, local/ is gated full data
```

## Build

```bash
python src/build.py --target public --fixtures   # CI-safe, allowlist-only
python src/build.py --target local  --fixtures   # full text, never published
python src/build.py --target public --benchmark ../../mortgage-benchmark/benchmark/v1_hmda2022/public_test.jsonl
```

The Pages publication uses the approved `v1_hmda2022` public test JSONL. Other local corpora
must be supplied through an explicit local build and are never published automatically.

## Why this exists

`generate.py` emitted one 53 MB HTML blob inlining every row of every source regardless
of license. That blob is tracked and pushed, and contains 2,000 rows of a dataset whose
own LICENSE file says no publication license has been selected.

This build cannot do that. `--target public` emits text only for sources whose ledger
entry is `publish_text` **and** whose license affirmatively permits redistribution; every
other source contributes counts and label distributions with text replaced by content
hashes. A source absent from the ledger is a build failure, not a default-permit.

**Exactly one source is approved:** `mortgage_benchmark_v1_hmda2022` under CC BY 4.0, so a
public build may emit its text with attribution. A passing fixture build still proves only that
the allowlist works, not that any particular release is authorized. Decisions live in
[`benchmarks/registry/distribution.yaml`](../../benchmarks/registry/distribution.yaml).
