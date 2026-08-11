# FAccT submission — *Benchmark Gains Are Not Governance Gains*

A conference-targeted paper for **ACM FAccT**, built on the same committed evidence surface as
`papers/unified-report/` but framed as an evaluation-validity and governance argument rather than a
technical report.

## What the paper argues

Safety guards are the mechanism by which a written content policy becomes an enforced decision, yet
they are selected by a rule nobody audits: fine-tune, score on a public suite, ship the best
checkpoint. The paper treats that selection rule as the object of study and shows, on one fixed panel
of four small open checkpoints, four places where a benchmark gain and the deployment claim come
apart — source validity, operational validity (alarm budget / ROC region / prevalence), regime
validity (self-host vs. hosted), and construct validity in a regulated domain. The deliverable is a
four-item **disclosure schedule**, not a new guard.

Track fit: *Evaluations and evaluation practices*.

## Format compliance (FAccT 2026 Author Guide)

| Requirement | Status |
| --- | --- |
| `\documentclass[manuscript,screen,review,anonymous]{acmart}` | verbatim as prescribed |
| ≤ 14 content pages incl. figures and tables | **14** (pp. 1–14) |
| 1 additional endmatter page | **1** (p. 15) — forced with `\clearpage` so the count is unambiguous |
| References, unlimited | pp. 16–18 |
| Appendices, excluded from the limit | pp. 18–24 |
| Generative AI Usage Statement | present, in the endmatter |
| Ethical Considerations / Adverse Impacts | present, in the endmatter |
| Identifying endmatter (contributions, acknowledgements, competing interests, positionality) | omitted for review, as required |
| Substantive limitations in the **main body** | §9, plus per-result caveats in place |
| Anonymised | no author, no affiliation, no repository URL; the companion report and the benchmark are cited as `Anonymous` |

**Line numbers are suppressed.** The class-option string the Author Guide prescribes is kept verbatim;
`\makeatletter\@ACM@reviewfalse\makeatother` immediately after `\begin{document}` turns off only the
line-numbering side effect of the `review` option.

## Where the numbers come from

No number in the paper is hand-typed. Every quantity is one of:

1. **A generated macro** `\input` from `../unified-report/generated/*.tex` (e.g. `\RepDelta`,
   `\MatchedTransferSft`, `\LowFprTransPAucDelta`, `\HtwoAggDeltaTpr`, `\Mort*`, `\Repro*`).
2. **A generated tabular/table** `\input` unmodified from the same directory — `tab_primary_gen`
   in the main text, and in Appendix D the verbatim `tab_sensitivity_gen`, `tab_matched_fpr_gen`,
   `tab_lowfpr_gen`, `mortgage_baseline_table`, `mortgage_composition_table`, `expguard_table`, and
   the worked case study `mortgage_case_study`.
3. **A figure plotted by `figures/make_facct_figures.py`**, which *parses* those same committed
   artifacts rather than taking literals. If a value cannot be recovered from a committed artifact the
   script exits non-zero instead of falling back.

Two generated artifacts expect anchors that this paper supplies rather than the unified report:
`tab_matched_fpr_gen` cites `tab:sensitivity` and `sec:matched-fpr-limits`, and `mortgage_case_study`
cites `sec:actIV-mortgage-pairs` and `sec:roadmap`. All four labels exist here, so the verbatim
artifacts resolve correctly.

## Figures

Generated into `figures/` by `make_facct_figures.py`:

| File | Used as | Content |
| --- | --- | --- |
| `fig_facct_findings.pdf` | Fig. 1 (main) | the four findings in one 4-panel spread |
| `fig_facct_budget.pdf` | Fig. 2 (main) | held-out and HarmBench recall at three thresholds |
| `fig_facct_gate.pdf` | Fig. 4 (main) | the protected-pair gate audited on both score scales |
| `fig_facct_casestudy_ranks.pdf` | Fig. 5 (appendix) | the worked G0/D1 miss, as a rank |
| `fig_facct_region.pdf` | *not currently placed* | graph form of Table 2; swap in if a page frees up |

Figure 3 is a TikZ regime map drawn inline. The paper is at the page limit, so the metric-region
result is carried by Table 2 rather than by `fig_facct_region.pdf`; the two show the same panel means.

Regenerate with:

```bash
../../.venv/bin/python figures/make_facct_figures.py
```

## Build

```bash
make pdf        # regenerates figures, then builds main.pdf
make figures    # figures only
make clean
```

The `Makefile` prefers a system `tectonic` and otherwise falls back to the bundled binary.

## Before submitting

- Re-run `make pdf` and confirm the content still ends on page 14 and the endmatter occupies page 15.
- Replace the anonymised `anon2026companion` / `anon2026benchmark` entries and the withheld
  repository URL in Appendix F for the camera-ready.
- Add the identifying endmatter sections (author contributions, acknowledgements, competing
  interests, positionality) only after acceptance.
