---
name: portfolio-watch
description: Use this skill when the user wants to turn a portfolio, watchlist, model portfolio, holdings list, or ticker list into a continuing Alva Portfolio Watch Playbook, dashboard, automation, or alert workflow. Trigger only for portfolio-centered monitoring with durable UI, refresh, subscription, remix, or alert intent; do not trigger for one-off financial analysis, generic macro/KOL/theme monitoring, backtests, trading execution, target prices, or position advice.
---

# Portfolio Watch

Portfolio Watch turns a group of assets into a safe, feed-backed Alva observation workflow. It helps the agent route the request, extract portfolio requirements, preflight data coverage, create a reusable config, design feeds and alerts, build a Playbook surface, and verify boundaries.

This skill is intentionally narrow: portfolio / watchlist / model portfolio observation only. Do not expand it into a general finance monitor.

## Public Package Note

This public package contains reusable skill instructions, references, examples,
and local validators. It does not contain private Alva dogfood artifacts,
owner namespaces, production ids, notification history, API tokens, brokerage
data, or real account connections.

For real Alva platform work, use the requesting user's own Alva namespace,
current Alva CLI help, Data Skills permissions, and base Alva platform
contracts. Do not reuse validation ids, URLs, paths, or notification evidence
from another user or repository.

## Required Context

Before real Alva platform work, read the base Alva skill and its owner references:

- `.agents/skills/alva/SKILL.md`
- `.agents/skills/alva/references/request-routing.md`
- `.agents/skills/alva/references/playbook-creation.md`
- `.agents/skills/alva/references/feed-lifecycle.md`
- `.agents/skills/alva/references/push-notifications.md`
- `.agents/skills/alva/references/content-legitimacy.md`

This is a platform-contract dependency, not an extra trigger condition. A user
does not need to mention the base `alva` skill for Portfolio Watch to proceed.
Route from the portfolio/watchlist request first, then read the base Alva files
only because real feed, Playbook, release, and push work must obey those
platform gates.

For this skill, load only the reference files needed for the current step:

| Need | Read |
| --- | --- |
| Decide trigger vs non-trigger | `references/request-routing.md` |
| Extract holdings, weights, privacy, defaults | `references/requirement-extraction.md` |
| Decide Full / Lite / Disabled | `references/data-preflight.md` |
| Build config, feed contract, page, README | `references/playbook-build.md` |
| Design quiet/push alert behavior | `references/alert-policy.md` |
| Verify and report evidence | `references/validation-checklist.md` |

## Workflow

1. Route the request. Trigger only when the user has a portfolio/watchlist/ticker-list object and asks for ongoing observation, UI, automation, release, remix, subscription, or alerts.
2. Extract requirements into `portfolio-watch.config.json`: assets, weights or no-weight mode, portfolio nature, observation goals, alert preferences, cadence, language, visibility intent, and privacy signals.
3. Apply defaults instead of interrogating the user. Ask at most one blocking question only when privacy, real publication, critical scope, or data source safety is unclear.
4. If explicit weights are provided, validate the weight total before any market fetch. Weighted mode requires exactly 100% within tolerance; do not silently normalize. Compute `weightedContributionPct = weightPct / 100 * oneDayMovePct` and reconcile the sum to summary `portfolioMovePct`.
5. Run capability and data preflight. Classify the build as `Full`, `Lite`, or `Disabled`; never fake coverage to preserve the original scope.
6. Build the smallest viable artifact: config, feeds/automation plan, Playbook UI contract, Alert contract, README, and Remix guide.
7. For real Alva builds, run at least two feed/automation executions before final screenshot or report when tabular groups use `@last/N`; the Playbook must filter rows by the latest summary `runId`.
8. If using real Alva, satisfy the base Alva hard gates before feed release, Playbook draft/release, lint, screenshot, and push verification.
9. Verify route samples, requirement extraction, preflight modes, page data reads, alert quiet/push logic, README boundaries, latest-batch no-duplicate rows, contribution reconciliation, and remaining risks.

## Independent Dogfood Standard

Use this standard when validating the skill itself or proving that it works
from a standalone `portfolio-watch` trigger.

1. Record that only `portfolio-watch` was explicitly triggered.
2. Read this file, the root README / validation report, previous dogfood
   reports, and only then read base Alva owner references as platform gates.
3. Create a fresh dogfood directory under `dogfood/<name>/`; do not overwrite a
   previous run.
4. For weighted portfolios, persist the exact user weights in config, prove the
   total is 100%, and write the validated weights into Data Health.
5. Use real Data Skills or feed output for every visible financial value.
6. Create and run a real feed, release the feed, create an active automation,
   write a feed-backed draft Playbook, run lint, capture a screenshot, and
   verify page/feed consistency.
7. Prove latest `runId` batch isolation: holdings/events/health rows for the
   latest run must contain expected rows exactly once, with no mixed prior
   batches.
8. If public Playbook release, visibility changes, real subscriptions, visible
   push, deletion, real accounts, or trading would be needed, stop for explicit
   confirmation. Without that authorization, label the result `L2/Lite`, not
   `Full`. With explicit authorization, keep subscription and visible-push
   tests scoped to the owner or named test subjects, and prove delivery with
   platform subscription state plus notification history.
9. Write a report with commands, IDs, URLs, paths, screenshots, run IDs, sidecar
   evidence, subscription/push evidence, fixes made, and remaining boundaries.

## Safety Rules

- Do not provide buy/sell/hold recommendations, target prices, position sizing, rebalancing instructions, or trade execution.
- Do not connect real brokerage accounts or use trading surfaces unless the user separately confirms a different trading task.
- Do not assume `portfolio` means real holdings. Classify as public template, watchlist, simulated portfolio, real holdings, or unknown.
- Do not assume `portfolio` means private. Use privacy signals: real holdings, cost basis, account identifiers, personal thesis notes, or private weights default to private or require confirmation.
- Do not display financial values unless they come from Data Skills, released feed output, or validated BYOD wired into the pipeline.
- Do not hardcode current prices, returns, contributions, event dates, estimates, fundamentals, or alert facts in HTML, README, or reports.
- If Alva data/API/platform ability is missing, downgrade to `Lite` or `Disabled` and record the evidence.

## Completion Standard

A Portfolio Watch delivery is complete when the package or Playbook includes a readable `SKILL.md`, required references, reusable config, generated example Playbook or prototype, README, brief, validation report, and evidence for route behavior, extraction, preflight, page data reading, alert policy, and content boundaries.

If a real Alva Playbook is published, completion additionally requires a fresh feed run, feed release, active cronjob evidence, `alva lint playbook`, screenshot showing feed-backed data, page/feed consistency, README currentness, visibility sanity, and alert sidecar verification.

If a real Alva Playbook is kept as draft because publication/subscription/push
authorization is absent, completion may be `L2/Lite` only. It still requires a
released feed, active automation, fresh run, draft URL, screenshot, lint,
README, Remix Guide, sidecar evidence, and machine revalidation.
