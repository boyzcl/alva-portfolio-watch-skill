# Data Preflight

Use this file before promising a Portfolio Watch Playbook. The goal is to decide what can be built without fabricating data.

## Preflight Inputs

Check these capabilities for the configured portfolio:

- Symbol normalization and duplicate handling.
- Covered asset type and market.
- Price and daily/intraday move data.
- Weight validation and weight or equal-weight contribution calculation. In explicit weighted mode, weights must total 100%; do not auto-normalize unless the user explicitly asks.
- Benchmark data, if configured.
- Earnings/event calendar or other event clue source.
- Optional fundamentals/estimates/news coverage when enabled.
- Feed read/write/release ability for durable Playbooks.
- Push sidecar ability if alerts are required.

For real Alva work, use Data Skills discovery and current CLI help from the base Alva skill. Do not rely on remembered endpoint names.

## Modes

| Mode | Criteria | Delivery |
| --- | --- | --- |
| `Full` | Core symbols are recognized; price/move data is available; contribution or watchlist summary can be computed; benchmark is available if claimed; at least one event source is available; feed, Playbook read, and alert sidecar can be verified. | Full Portfolio Watch Playbook with overview, holdings table, event watch, alert center, data health, README, and Remix guide. |
| `Lite` | Symbols and basic price/watchlist data are available, but events, fundamentals, news, push, or some asset coverage are missing. | Lightweight Playbook with portfolio status, holdings/watchlist, available data health, and only verified alerts; disabled modules are hidden or labeled. |
| `Disabled` | Core symbols cannot be resolved, required price data is unavailable, feed cannot run/read, or alert cannot be verified while alert is central to the goal. | Do not publish a fake complete Playbook. Return a blocker report and a minimal downgrade proposal. |

## Failure Handling

- More than 20% unresolved symbols is a data-quality blocker unless the user accepts a narrower universe.
- Explicit weighted mode with weights that do not total 100% is a configuration blocker until corrected.
- Weighted contribution is available only when every included symbol has a real price move and a validated weight; otherwise downgrade or disable the contribution module instead of filling zeros.
- Do not replace missing values with synthetic rows or `live: false` data.
- Do not remove missing symbols silently; show them in Data Health.
- Do not claim event/news/fundamentals sources in README unless those sources are wired and verified.
- If push cannot be verified, keep alert UI in quiet/simulation status and mark push setup incomplete.

## Example Classification

| Case | Expected |
| --- | --- |
| `NVDA, MSFT, AAPL, AMZN, META, QQQ` with US equities/ETF coverage and public template intent | `Full` candidate, subject to live Data Skills/feed verification. |
| No-weight focus pool with covered US tickers but no event/push setup yet | `Lite` until event/push coverage is verified. |
| Duplicate symbols plus invalid symbols plus unsupported asset classes | `Disabled` or reduced `Lite`, with failing ids listed. |

Mode labels are evidence labels, not marketing labels. If evidence is local-only, say `Full candidate` instead of `Full released`.
