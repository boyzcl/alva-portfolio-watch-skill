# Portfolio Watch Skill Quality Score

Current strict score: `9.8 / 10`.

This score evaluates whether `portfolio-watch` can guide an agent from a
portfolio/watchlist/model-portfolio request to a safe, real, verifiable Alva
Portfolio Watch workflow.

## Rubric

| Dimension | Points | Current |
| --- | ---: | ---: |
| Trigger boundary is clear and does not route one-off analysis, macro monitors, backtests, trading, target prices, or position advice into this skill. | 1.0 | 1.0 |
| Independent trigger path is clear; the user does not need to explicitly name the base Alva skill. | 1.0 | 1.0 |
| Requirement extraction covers assets, weights, portfolio nature, privacy, visibility intent, cadence, language, and alert needs. | 1.0 | 1.0 |
| Data preflight and downgrade behavior can classify Full, Lite, or Disabled without fabricating missing data. | 1.0 | 1.0 |
| Weighted portfolio support includes exact 100% weight validation, weighted contribution, portfolio move, benchmark, and reconciliation. | 1.0 | 1.0 |
| Real Alva build guidance covers Data Skills, feed, automation, feed release, Playbook draft/release, README, Remix Guide, lint, and screenshots. | 1.0 | 1.0 |
| Alert and notification boundaries cover quiet-first behavior, sidecars, publisher push, subscription, visible-push authorization, and owner/test-only delivery evidence. | 1.0 | 0.95 |
| Validation system covers local structure, route tests, preflight cases, page data reads, alert policy, latest `runId` batch isolation, page/feed consistency, and no duplicate rows. | 1.0 | 0.95 |
| Safety and content legitimacy prevent buy/sell advice, target prices, position sizing, rebalancing instructions, trading execution, and invented financial values. | 1.0 | 1.0 |
| Reusability and maintainability include clear references, examples, reports, validation scripts, and a public package boundary. | 1.0 | 0.9 |

## Why It Scores Above 9.5

The skill has passed three progressively stricter validations:

1. A real `L2/Lite` watchlist dogfood.
2. A real weighted-portfolio `L2/Lite` dogfood.
3. An authorized `Full-path` dogfood including public Playbook release,
   public visibility, owner-scoped subscription, and owner-scoped visible push.

The public package also includes a validator that checks package structure,
route behavior, preflight classification, alert logic, fixture-based page
wiring, README boundaries, and absence of private dogfood identifiers.

## Remaining Deductions

- `-0.1`: real dogfood has focused on US equity/ETF portfolios. Non-US
  equities, crypto, mixed-asset portfolios, paid/private visibility, group
  subscriptions, and BYOD variants need separate validation.
- `-0.1`: platform notification history can be feed-scoped after Playbook
  subscription cascade. The skill documents this, but it remains a gotcha that
  future agents must verify carefully.

## Public Release Judgment

The skill is suitable for public release as a sanitized package. It should not
include private dogfood directories, personal namespaces, notification history,
production ids, local filesystem paths, secrets, or brokerage/account data.

