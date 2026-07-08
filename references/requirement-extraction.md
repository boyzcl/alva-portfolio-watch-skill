# Requirement Extraction

After routing succeeds, convert the user request into a configuration contract before writing runtime code or HTML.

## Required Fields

Extract or default these fields:

| Field | Meaning |
| --- | --- |
| `portfolioName` | Human-readable name for the portfolio/watchlist. |
| `visibilityIntent` | `public_template`, `public_release`, `private_personal`, `draft_only`, or `needs_confirmation`. |
| `language` | `zh-CN` or `en-US`; follow the user's language when unclear. |
| `portfolioNature` | `real_holdings`, `simulated_portfolio`, `watchlist`, `public_template`, or `unknown`. |
| `mode` | `weighted_portfolio`, `equal_weight`, or `watchlist_only`. |
| `symbols` | Asset list with symbol, asset type, market, optional weight, core flag, and notes. |
| `benchmark` | Optional comparison asset; default `QQQ` for US growth/tech examples, otherwise ask only if required. |
| `observationGoals` | Price change, contribution, concentration, event watch, earnings, news/event clues, data health. |
| `refreshCadence` | Default `daily`; use event-driven only when the user asks. |
| `alertRules` | Price move, portfolio move, event window, cooldown, stale suppression, weak-evidence suppression. |
| `privacySignals` | Real holdings, cost basis, account id, private thesis notes, personal weights, or unknown sensitivity. |

## Defaults

- No weights: choose `watchlist_only` when the user says watchlist/focus pool; choose `equal_weight` only when contribution or portfolio summary is requested.
- Explicit weights: choose `weighted_portfolio`; preserve each supplied weight as user-provided or simulated input, validate the total equals 100% within a tiny tolerance, and block rather than renormalize silently when the total is wrong.
- No cadence: use daily refresh.
- No alert threshold: push only material changes; quiet run otherwise.
- No language: match current user language.
- No visibility: public-template only when no sensitive fields exist; otherwise `needs_confirmation`.
- Missing data: show Data Health and downgrade; never delete symbols silently.

## Privacy Decision

| Evidence | Default |
| --- | --- |
| Public sample/template/watchlist | Can publish public after gates pass. |
| Real holdings, cost basis, account, private notes, personal weights | Private or confirmation before public release. |
| User explicitly asks to share publicly | Public only after removing sensitive fields. |
| Sensitivity unclear | Ask one blocking privacy question. |

## Configuration Output

Write `portfolio-watch.config.json` with stable schema keys. Keep facts separate:

- User intent and weights belong in config.
- Financial market values belong only in Data Skills/feed/BYOD outputs.
- AI summaries belong in labeled narrative fields, not factual table columns.

## Extraction Checks

For validation, run at least:

1. Weighted standard portfolio: extracts symbols, weights, benchmark, daily cadence, weight total 100%, simulated-vs-real boundary, Full candidate.
2. No-weight watchlist: defaults to `watchlist_only` or `equal_weight` with explicit copy.
3. Abnormal portfolio: preserves bad/unsupported symbols for Data Health instead of deleting them.
