# Portfolio Watch Request Routing

Use this file before invoking Portfolio Watch. The route is based on the user's intended artifact, not on isolated finance keywords.

## Trigger

Trigger Portfolio Watch only when all three conditions are true:

1. The object is a group of assets: portfolio, holdings list, model portfolio, watchlist, ticker list, ETF basket, or focus pool.
2. The user wants ongoing observation: track, monitor, watch, refresh, update, subscribe, alert, or revisit.
3. The user wants a durable artifact: Alva Playbook, dashboard, automation, feed, shareable template, remixable page, or notification.

Typical triggers:

- "把这些 ticker 做成一个每天刷新的 Portfolio Watch Playbook。"
- "给我的自选股组合生成一个带 Alert 的 Alva 页面。"
- "我有一组模拟持仓，想看每日贡献、事件和提醒。"
- "把 NVDA, MSFT, AAPL, AMZN, META, QQQ watch 起来。"
- "做一个可分享的组合观察模板，别人能 remix 成自己的组合。"

## Non-Trigger

Do not trigger Portfolio Watch for these requests:

| Request | Route |
| --- | --- |
| Single-asset question, valuation, "why did it move" | Financial Analysis / Ask Question |
| One-off portfolio analysis with no ongoing UI/refresh/alert | Financial Analysis / Ask Question |
| CPI/FOMC/macro alert with no portfolio object | Macro/event monitor route |
| KOL/X/news monitor with no portfolio object | Content/social monitor route |
| Theme chain monitor such as AI infrastructure or oil chain | Theme Playbook route |
| Backtest, signal, rebalance, target allocation, trade execution | Altra / Strategy / Trading route |
| Connect real brokerage account or place orders | Trading execution route with explicit confirmation |

## Routing Heuristics

- "portfolio" alone is not enough. If the user asks a one-time question, answer directly with provenance.
- "alert" alone is not enough. If no portfolio object exists, use the relevant event/content/market monitor route.
- "watchlist" plus "dashboard", "refresh", "alert", "subscribe", "share", or "Playbook" is enough.
- If the user asks for a public template and the input has no sensitive fields, default to public-template intent.
- If privacy is unclear and the request may include real holdings, ask exactly one question: "这是公开关注组合/示例组合，还是包含真实个人持仓、成本或私密笔记？"

## Route Test Set

Use these examples in validation:

| Input | Expected |
| --- | --- |
| "帮我把 NVDA/MSFT/AAPL 做成每天更新、有提醒的 Playbook" | trigger |
| "我有一组持仓，想每天看贡献和风险，异常时提醒" | trigger |
| "做一个可分享的 AI leaders 关注组合模板" | trigger |
| "NVDA 现在怎么看？" | no_trigger |
| "监控 CPI 和 FOMC，突破时提醒" | no_trigger |
| "回测一个组合再平衡策略" | no_trigger |
| "连接我的券商账户并自动调仓" | no_trigger |

Completion: route only when the expected artifact is portfolio-centered monitoring, not general finance monitoring.
