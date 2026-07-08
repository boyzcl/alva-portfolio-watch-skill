# Alva Portfolio Watch Skill

[中文说明](README.zh-CN.md) | English

`portfolio-watch` is a Codex/Agent skill for turning a portfolio, watchlist,
model portfolio, holdings list, or ticker list into a safe, feed-backed Alva
Portfolio Watch workflow.

It is designed for ongoing observation: Playbooks, dashboards, automations,
alerts, subscriptions, and remixable portfolio templates. It is not a trading
or investment-advice skill.

## What It Builds

- Portfolio or watchlist requirement extraction.
- Full / Lite / Disabled data preflight.
- Weighted portfolio validation with exact 100% weight checks.
- Weighted contribution and portfolio move reconciliation.
- Feed-backed Playbook UI contract.
- Data Health and provenance boundaries.
- Quiet-first alert and push-notification policy.
- README and Remix Guide requirements for released Playbooks.
- Local validation for routing, config, alert logic, page wiring, and public
  package hygiene.

## When To Use

Use this skill when the user provides a group of assets and asks for durable
monitoring, refresh, alerts, subscription, sharing, or a Playbook.

Do not use it for:

- One-off market or portfolio analysis.
- Single-stock questions.
- Macro/KOL/theme monitoring without a portfolio object.
- Backtests, signals, rebalancing, target allocations, or trade execution.
- Buy/sell/hold recommendations, target prices, or position-sizing advice.

## Safety Rules

- This skill only creates observation workflows.
- It does not provide 买卖建议, 目标价, 仓位建议, 调仓建议, or trading execution.
- It is 非投资建议 and should be presented as portfolio observation only.
- User-visible financial values must come from Alva Data Skills, released Alva
  feed output, or validated BYOD wired into the feed pipeline.
- Local examples intentionally contain no live prices, returns, event dates,
  estimates, news, or fundamentals.
- If explicit weights are provided, they must total exactly 100% within the
  configured tolerance. Do not silently normalize.
- If data coverage, feed release, subscription, or push verification is missing,
  downgrade to Lite or Disabled and explain the evidence.
- Treat privacy explicitly: public template portfolios can be published only
  when safe, while private holdings, cost basis, account identifiers, or
  personal notes require private handling or fresh confirmation.

## Requirements

For local package validation:

- Python 3.10+

For real Alva builds:

- Alva CLI access.
- Alva Data Skills permissions.
- A working Alva namespace.
- The base Alva skill installed alongside this skill, or equivalent platform
  contract docs for feed lifecycle, Playbook release, content legitimacy, and
  push notifications.

## Package Layout

```text
alva-portfolio-watch-skill/
  SKILL.md
  README.md
  README.zh-CN.md
  LICENSE
  portfolio-watch.config.json
  agents/openai.yaml
  references/
    request-routing.md
    requirement-extraction.md
    data-preflight.md
    playbook-build.md
    alert-policy.md
    validation-checklist.md
  examples/
    no-weight-watchlist.config.json
    abnormal-portfolio.config.json
    portfolio-watch-playbook/
      index.html
      README.md
      portfolio-watch-sample-feed.json
      browser-verification.json
      prototype-screenshot.png
  scripts/
    validate_portfolio_watch_skill.py
  docs/
    VALIDATION_SUMMARY.md
    VALIDATION_SUMMARY.zh-CN.md
    QUALITY_SCORE.md
```

## Validate Locally

```bash
python3 scripts/validate_portfolio_watch_skill.py --write-report
```

The validator checks:

- Required files and references.
- Route / non-route examples.
- Full candidate / Lite / Disabled preflight cases.
- Alert quiet / push-candidate logic.
- Local prototype fixture wiring.
- README boundary wording.
- Public-release hygiene, including absence of private dogfood identifiers.

## Real Alva Dogfood

This public repository includes a sanitized validation summary, not private
Alva run artifacts. To claim a new Full-path validation, run the workflow in
your own Alva namespace and record:

- Alva preflight and CLI help checks.
- Data Skills coverage checks.
- At least two feed or automation executions.
- Released feed and active automation.
- Feed-backed Playbook draft/release.
- `alva lint playbook` result.
- Screenshot of the released Playbook.
- Latest `runId` batch isolation and no duplicate rows.
- Weighted contribution sum equals portfolio move.
- README, Remix Guide, Data Health, and alert sidecar evidence.
- If authorized: public visibility, subscription state, and visible push
  notification history limited to owner/test users.

## License

MIT.
