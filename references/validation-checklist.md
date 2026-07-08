# Validation Checklist

Use this file before claiming Portfolio Watch is complete.

## Package Checks

- `SKILL.md` exists, has frontmatter, and contains no TODO placeholders.
- Required references exist.
- `portfolio-watch.config.json` exists and is valid JSON.
- A generated example Playbook or prototype exists.
- README, validation report, and one-page brief exist.

## Route Checks

Run trigger and non-trigger examples from `request-routing.md`. Expected:

- Portfolio/watchlist + durable UI/refresh/alert intent triggers.
- One-off asks, macro-only monitors, KOL-only monitors, theme-only monitors, backtests, and trading execution do not trigger.

## Requirement Checks

Validate:

- Standard weighted portfolio.
- No-weight watchlist/focus pool.
- Abnormal portfolio with invalid, duplicate, or unsupported symbols.

Output should preserve missing/problem symbols in Data Health rather than deleting them.

For weighted mode, also validate:

- Config weights sum to 100%.
- Feed rejects non-100 weights instead of silently normalizing.
- Latest-batch holdings contain the expected symbols exactly once.
- Sum of `weightPct` equals 100.
- Sum of `weightedContributionPct` equals summary `portfolioMovePct`.
- Benchmark value is present if the README or UI claims it.

## Preflight Checks

Cover `Full`, `Lite`, and `Disabled`:

- `Full` can be a live-verified mode only after Data Skills/feed/Playbook/Alert checks pass.
- Local-only validation should label it `Full candidate`.
- `Lite` must identify unavailable modules.
- `Disabled` must explain blockers and next viable downgrade.

## Page And README Checks

- HTML reads a data file/feed at runtime.
- HTML contains no hardcoded current financial values.
- HTML filters tabular feed outputs to the latest `runId` / batch and does not mix rows across multiple feed runs.
- After at least two feed runs, the page shows exactly the latest expected symbol/event/health rows with no cross-run duplicates.
- Weighted pages show contribution values from feed output and reconcile them with the summary portfolio move.
- Data Health and provenance are visible.
- README states sources, freshness, blind spots, privacy, remix path, and non-advisory boundary. For Chinese surfaces, the boundary should include the exact idea of `非投资建议`.
- README does not claim unwired data sources, live refresh, push delivery, or public/private state that has not been verified.

## Alert Checks

- Calm run emits `<|SKIP_NOTIFICATION|>`.
- Material run emits a push candidate only with fresh data.
- Stale data suppresses push.
- Cooldown suppresses repeated push.

## Real Alva Release Checks

If a real Playbook is published, attach evidence for:

- Fresh feed run.
- Feed release after sidecar addition.
- Active cronjob.
- Public/private visibility matches privacy signals.
- Public release has a canonical share URL, and `playbooks get` reports the
  intended visibility.
- Playbook/feed subscription state is ACTIVE for the owner or explicit test
  subject when subscription is part of the authorized validation.
- `alva lint playbook` pass or documented bypass.
- Screenshot shows feed-backed values.
- Page values match feed output.
- Screenshot is taken after a second fresh run or triggered automation when possible, so latest-batch filtering is exercised.
- Alert sidecar writes fresh quiet or push record.
- Visible push, when authorized, has notification-history evidence with
  `status=sent`, target user limited to the owner/test subject, and copy that is
  verification/observation-only and non-investment-advice. If a later run is
  quiet after a one-shot visible test, record both the sent history and latest
  quiet sidecar instead of treating the quiet latest run as failure.

If these cannot be verified, mark real release as not performed or blocked.
