# FAccT 2026 readiness review

Date reviewed: 2026-08-16  
Submission artifact reviewed: `papers/facct/main.pdf` (there is no `article.pdf` in this checkout)  
Scope: `papers/facct/`, the generated artifacts it imports, and the claim-bearing analysis code in `papers/unified-report/`.

## Venue standard and status

The [FAccT 2026 Author Guide](https://facctconference.org/2026/authorguide.html) requires an anonymous ACM `acmart` submission, a maximum of 14 single-column content pages including figures and tables, unlimited references, and at most one additional page used only for endmatter. The main paper must stand without the appendices. It requires a generative-AI usage statement, omits identifying endmatter during anonymous review, and treats violations of anonymity, formatting, length, ACM policy, and dual-submission policy as possible desk-rejection grounds.

The guide and the [2026 CFP](https://facctconference.org/2026/cfp.html) evaluate relevance, rigor and clarity, originality, and potential impact. The most appropriate focus area is **Evaluations and evaluation practices**. The paper also speaks to the CFP's science of responsible AI evaluation and governance, assurance testing, deployment policies, and transparency documentation. FAccT's CFP warns that work without deep engagement with the social components of computational systems is out of scope; this is the principal venue-fit test for this paper.

The 2026 submission deadline (2026-01-13 AoE) and conference dates (2026-06-25 to 2026-06-28) have passed. This review therefore assesses the artifact against the 2026 standard; it cannot make the work submittable to that already closed venue.

## Baseline score: 76/100

The score is a readiness assessment, not a predicted acceptance probability. It weights the criteria published in the FAccT author and reviewer guides, with extra weight on whether an empirical governance claim is supported by the evidence actually collected.

| Dimension | Weight | Baseline | Assessment |
| --- | ---: | ---: | --- |
| FAccT fit | 10 | 8 | A serious evaluation-practice contribution with deployment stakes; the social account remains thinner than the measurement account. |
| Originality | 10 | 7 | The four-part audit and evidence-tier discipline are a useful synthesis; the component ideas are established. |
| Significance and impact | 10 | 8 | The paper identifies a consequential failure in safety-guard selection, but has not shown that the schedule changes organizational practice. |
| Methodological rigor | 15 | 10 | Pairing, source separation, and explicit limits are strong; the published matched-FPR procedure could exceed its stated alarm budget under ties. |
| Research questions, claims, and evidence | 15 | 8 | The claims are mostly candid, but the fixed four-model panel, post-hoc frontier aggregate, and weak mortgage labels cap what the paper can establish. |
| FAccT/social and ethical analysis | 10 | 7 | It connects errors to users and procurement, but does not empirically study who has authority to set policy, bear errors, or use disclosures. |
| Positioning and bibliography | 8 | 6 | The FAccT foundation is sound, but the main-text positioning does not sharply distinguish the proposed schedule from adjacent documentation and audit practices. |
| Reproducibility and limitations | 8 | 6 | Generated-score provenance is unusually good; training/scoring and the stochastic mortgage construction are not reproducible, and the verifier leaves four generated inputs uncovered. |
| Narrative and prose | 8 | 7 | The problem, protocol, and negative result are clear; Q2 repeats a similar lesson three times while the governance warrant is comparatively compressed. |
| Figures and tables | 5 | 4 | The overview, budget, and worked-miss figures are effective. Several appendix tables are dense and main-text captions do substantial argumentative work. |
| Format and submission compliance | 5 | 5 | The source uses anonymous `acmart` review mode, the compiled artifact has 14 content pages plus endmatter, and the required endmatter is present. |

## Main rejection risks

1. **Retrospective evidence is asked to carry a governance prescription.** The schedule is plausible and useful, but the study does not show that it helps a decision-maker choose differently or avoid a consequential error in a real organizational setting.
2. **The regulated-domain instrument is exploratory.** It is LLM-judged, not SME/counsel adjudicated, has an empty G1/D0 quadrant, three scored protected pairs, and one pair crosses splits. It should not bear a claim about fair lending or a general claim about domain blindness.
3. **The generality claim is narrow.** Four checkpoints from two lineages, one manifest, and one LoRA recipe support a fixed-panel estimate, not a conclusion about safety-guard adaptation generally.
4. **The frontier regime reversal is not confirmatory.** The represented-source aggregation is post hoc, based on three purposively chosen sources, and changes under defensible reweighting.
5. **The matched-FPR headline was technically overstated.** A score quantile followed by `>=` can classify a whole tied negative-score block and exceed the intended budget. This review's correction changes the transfer result from 0.217 to 0.185 and HarmBench recall from 0.203 to 0.171; it does not reverse the qualitative conclusion.

## Revision completed in this branch

The branch corrects the matched-FPR reconstruction rather than merely qualifying it in prose.

- `threshold_at_most_fpr` now selects the least strict observed threshold whose empirical negative FPR is at or below the base budget, preserving tied score blocks whole.
- Regression tests cover an all-tied negative block and selection of the least strict feasible threshold.
- The claim-bearing generated table/macros and the FAccT figures were regenerated from the committed score matrix.
- The FAccT and unified-report text now accurately says “at or below” rather than “matches,” and removes the invalid quantile-sensitivity claim.
- The required generative-AI statement now names OpenAI Codex and limits its claimed role to code assistance and copy-editing.

## Reassessment after the verified correction: 78/100

The correction improves methodological rigor, evidence integrity, and reproducibility, but it cannot raise the work to 90 because it introduces no new independent data, stakeholder evidence, or prospective experiment. A score of 90 or above would be misleading.

| Dimension changed by this branch | Baseline | Revised | Reason |
| --- | ---: | ---: | --- |
| Methodological rigor | 10/15 | 11/15 | Matched-budget claims now obey the stated budget in the presence of ties. |
| Claims and evidence | 8/15 | 9/15 | Claim-bearing values and captions reflect the conservative calculation. |
| Reproducibility and limitations | 6/8 | 6/8 | The tie semantics are executable and regression-tested, but the full check now reports four generated inputs as uncovered. |
| Overall | 76/100 | 78/100 | No score increase is assigned for unrun proposals; the full regeneration exposed no basis for a reproducibility increase. |

## Human-authored revision required for a 90+ claim

FAccT 2026 prohibits LLM-generated publication text. The revisions below are deliberately an author-owned blueprint rather than generated manuscript prose. They are also the substantive work that remains between this artifact and a defensible 90+ readiness assessment.

### A. Turn the disclosure schedule into a sociotechnical contribution

Define precisely who uses each disclosure, what decision it changes, what authority they have, and whose interests are protected when the guard blocks or allows a request. The paper should state that disclosure is not governance by itself: it cannot determine legitimate policy, allocate decision rights, provide appeal or remedy, or replace participatory policy design. Position this limitation next to the schedule, not only in endmatter.

The minimum credible empirical upgrade is a pre-registered study with practitioners, auditors, procurement reviewers, or policy owners. Compare a conventional leaderboard packet with the proposed disclosure packet on a realistic guard-selection task. Measure changed selections, uncertainty, and the reasons participants give. Obtain the appropriate ethics review and describe participant recruitment, compensation, and limitations.

### B. Promote only evidence that has a matching warrant

Keep the fixed-panel result as the primary retrospective finding: *represented-source gains do not establish source-held-out performance on this panel*. Do not generalize to “fine-tuning harms guards.” State the frontier result as a regime-conditioned illustration, not a procurement rule. Keep the mortgage result as an instrument audit and worked example, not a fair-lending finding.

Replace any universal language about how guards are selected with either documented evidence about the relevant practice or a scoped claim about the evaluation pattern studied here. Separate descriptive results, normative recommendations, and future validation requirements visually and linguistically.

### C. Make the mortgage arm publishable as a FAccT resource

Commission independent SME/counsel adjudication of the policy cards and a stratified sample of labels; report the protocol, disagreements, and adjudication outcomes. Construct all four quadrants before evaluation, preserve protected pairs inside a split, and add D=1 minimal pairs that test coded versus plainly stated policy violations. Include the provenance, generator model/version, prompts, revisions, license, and a data-use policy. Until then, move this arm from a headline “finding” to a bounded case study.

### D. Add a sealed, pre-specified replication

Before accessing new scores, lock the model list, training recipe, suite membership, family/dependence structure, calibration split, FPR semantics, primary estimand, and multiplicity family. Use several model lineages and purpose-built guards. Evaluate the disclosure schedule on a genuinely sealed cohort and report all pre-specified outcomes, including nulls. This is the highest-leverage technical path to a stronger claim.

### E. Rebalance the 14-page main narrative

Retain the overview figure, the paired source-separation result, the conservative matched-budget result, and one bounded case study. Compress repeated explanations of ranking, prevalence, and alarm budgets. Use the released space for: (1) the sociotechnical decision model; (2) a claim--evidence--limit table in the main paper; and (3) a sharper account of what the disclosure schedule cannot do. Keep detailed generator mechanics, full generated tables, and the extended literature map in appendices, because reviewers are not obliged to read them.

### F. Bibliography and positioning audit

The current bibliography already includes core FAccT work on measurement, functionality, accountability, abstraction, model cards, datasheets, and sociotechnical harms. Before submission, authors should verify every recent guardrail preprint's title, author list, identifier, and availability; remove any source that cannot be verified. Add only literature that is used to make a specific distinction: problem formulation and the distribution of authority, audit/documentation limits, and sociotechnical evaluation of generative systems. Do not add citations merely to signal breadth.

## Verification gates for the next author revision

1. The main paper remains self-contained at no more than 14 content pages; endmatter occupies only its permitted page.
2. A clean anonymous build has no identifying metadata, repository identity, acknowledgements, contributions, competing interests, or positionality statement.
3. `python -m pytest -q tests/test_matched_fpr.py tests/test_operating_point.py` passes.
4. Rebuild generated matched-FPR artifacts and FAccT figures from committed scores; verify their diffs intentionally.
5. Compile with Tectonic, inspect the PDF visually, resolve overfull boxes and nontrivial underfull pages, and confirm no unresolved citations or references.
6. Extend the full reproduction check to cover the four currently uncovered generated inputs; until then, report its scope honestly.
