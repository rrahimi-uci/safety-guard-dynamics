# GitHub Copilot repository instructions

- You may work on assigned issues and development tasks, create a branch, and open a pull request. You must never merge a pull request, approve a pull request, push to `main`, or represent your review as human approval.
- Before opening or marking a pull request ready for human review, understand the issue acceptance criteria, implement the smallest complete change, and add or update tests for changed behavior.
- Run the repository CI-equivalent checks for affected areas from `.github/workflows/verify.yml` and `.github/workflows/pages.yml`. At minimum run the applicable registry, index, Markdown-link, pytest, explorer, benchmark, composition, distribution, and publication checks; run `git diff --check`.
- Keep validation deterministic and offline. Do not require credentials, network services, model calls, or uncommitted local data for ordinary tests.
- Do not submit a PR as ready if a required test, artifact, registry, publication, or build check fails. Preserve declared expected failures and report them explicitly; never silently weaken a gate.
- The PR body must list changed behavior, tests added or updated, every validation command and result, evidence tiers, limitations, risks, and publication/deployment implications.
- During code review, identify correctness, security, test-coverage, evidence-boundary, and publication issues and leave comments. Never approve or merge the PR.
