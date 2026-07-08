# Playbook Build Contract

Use this file after routing, extraction, and preflight. It defines the Portfolio Watch artifact shape.

## Build Order

1. Finalize `portfolio-watch.config.json`.
2. Define feed groups and schema.
3. Implement runtime feed logic or local prototype wiring.
4. Build a Playbook UI that reads feed output at runtime.
5. Write README and Remix guide from the actual data sources and cadence.
6. Validate alert behavior with `references/alert-policy.md`.
7. If publishing on Alva, satisfy the base Alva feed and Playbook hard gates.

## Feed Groups

Recommended feed groups:

| Group | Purpose |
| --- | --- |
| `portfolio/summary` | Mode, data freshness, portfolio move, benchmark context, top contributors. |
| `portfolio/holdings` | Symbol, display name, weight/equal-weight status, move, contribution, data status. |
| `events/watch` | Earnings, filings, announcements, or verified event clues tied to portfolio symbols. |
| `alerts/history` | Alert decision, message, quiet/push status, trigger and suppression reasons. |
| `health/coverage` | Source coverage, missing fields, stale data, permissions, limitations. |

All financial values in these groups must come from Data Skills, released feed outputs, or validated BYOD. The local prototype may use null values and fixture labels only; it must not pretend fixture values are market facts.

## Weighted Mode

For `weighted_portfolio`, validate weights before any market fetch. The feed should fail fast when the total is not 100% instead of normalizing silently.

Required fields:

- Summary: `totalWeightPct`, `weightValidated`, `portfolioMovePct`, `benchmarkMovePct`, top/bottom contributor symbols and contributions.
- Holdings: `weightPct`, `oneDayMovePct`, `weightedContributionPct`.
- Data Health: a weight-config row that states whether weights total 100% and that weights are observation inputs, not allocation advice.

Formula:

```text
weightedContributionPct = weightPct / 100 * oneDayMovePct
portfolioMovePct = sum(weightedContributionPct)
```

Validation must prove the latest run's holding weights sum to 100%, each contribution is present, and the contribution sum matches the summary portfolio move.

## Run-Scoped Batches

For tabular groups such as `portfolio/holdings`, `events/watch`, `alerts/history`, and `health/coverage`, every record from one feed execution should include the same `runId` or batch identifier. The summary group should also expose that `runId`.

The Playbook page should read the latest summary first, then render only rows whose `runId` matches the latest summary. Do not render a broad `@last/N` result directly as a table, because after two or more feed runs it can mix the newest batch with older rows and duplicate symbols or health entries.

Validation must include at least two feed runs before screenshotting the page, or an equivalent fixture that proves the page filters to the latest batch.

## UI Modules

MVP modules:

- Portfolio Overview: answers whether anything important changed today.
- Holdings / Watchlist Table: shows symbol, weight mode, data status, and verified values when available.
- Event Watch: shows upcoming or recent verified portfolio-relevant events.
- Alert Center: shows rules, last decision, quiet/push state, cooldown, and suppression.
- Data Health: shows sources, freshness, coverage gaps, and permissions.
- Methodology / Boundary: explains provenance, refresh, limitations, and non-investment-advice boundary.
- Remix Guide: tells users what to replace and what to preserve.

## Browser Data Rule

For real Alva Playbooks, HTML must load `AlvaToolkit.AlvaClient` and read feed paths in the viewer browser. Do not hardcode financial values in inline JavaScript or HTML. Do not fetch raw Alva APIs with guessed origins or hand-written auth headers.

For local prototypes, use a clearly labeled fixture file with no fabricated market values. The prototype should prove data wiring and empty/disabled states, not market accuracy.

## README Contract

The README must state:

- What portfolio/watchlist this observes.
- Whether it is public template, simulated, watchlist-only, or private personal.
- Which data sources are actually wired.
- Refresh cadence and what "fresh" means.
- Which modules are Full, Lite, or Disabled.
- How alerts decide push vs quiet.
- Privacy boundary and public/private guidance.
- Non-investment-advice boundary.
- Remix instructions.

README claims must match actual config, feeds, deployment, and verified capabilities.

For Chinese user-facing README text, include an explicit `非投资建议` boundary plus the concrete banned actions: no buy/sell advice, target prices, position sizing, rebalancing, or trade execution.
