# Alva Portfolio Watch Skill 中文说明

[English README](README.md) | 中文说明

`portfolio-watch` 是一个面向 Codex / Agent 的公开 Skill，用来把投资组合、自选股、模拟组合、持仓列表或 ticker 列表，转成安全、可验证、feed-backed 的 Alva Portfolio Watch 工作流。

它适合做持续观察：Playbook、dashboard、automation、alert、subscription，以及可 remix 的组合观察模板。它不是交易工具，也不是投资建议工具。

## 它解决什么问题

很多金融 Agent demo 会停在“一次性回答”或“静态页面”。`portfolio-watch` 的目标是把一个组合观察需求变成可运行、可追踪、可发布、可复验的 Alva 工作流：

- 从用户输入中抽取组合、权重、隐私、可见性、刷新频率和提醒需求。
- 在承诺发布前做 Data Skills / feed / alert 预检。
- 判断当前只能做 `Full candidate`、`Lite` 还是 `Disabled`。
- 对显式权重组合做 100% 总权重校验。
- 计算 weighted contribution，并和组合加权日变动对账。
- 生成 feed-backed Playbook 的页面契约、README 和 Remix Guide。
- 通过 Data Health 说明数据来源、覆盖情况和缺口。
- 使用 quiet-first alert 策略，只有满足证据、freshness、cooldown 和授权条件时才验证可见 push。

## 什么时候使用

当用户给出一组资产，并且希望持续观察、刷新、提醒、订阅、分享或发布成 Playbook 时，使用这个 Skill。

典型输入：

```text
帮我把 NVDA/MSFT/AAPL/AMZN/META/QQQ 做成一个每天更新、有提醒的 Portfolio Watch Playbook。
```

```text
我有一组模拟持仓，想看每日涨跌贡献、事件窗口和 Data Health，并且未来可以 remix。
```

```text
做一个可分享的 AI leaders 关注组合模板，别人能复制后换成自己的 ticker。
```

## 不适用场景

不要把这个 Skill 用在这些任务上：

- 单只股票怎么看。
- 一次性的市场或组合分析。
- 没有组合对象的 CPI / FOMC / 宏观事件监控。
- 没有组合对象的 KOL / X / 新闻 / 主题链监控。
- 回测、信号、再平衡、目标仓位、真实账户连接或交易执行。
- 买入、卖出、持有建议。
- 目标价、仓位建议、调仓建议。

## 安全边界

这个 Skill 只做组合观察，不做投资决策。

- 非投资建议。
- 不输出买卖建议。
- 不输出目标价。
- 不输出仓位建议。
- 不输出调仓建议。
- 不接入真实券商账户。
- 不执行交易。
- 不把 LLM 记忆、网页搜索片段或用户粘贴的示例当作金融事实。
- 所有用户可见金融值必须来自 Alva Data Skills、released Alva feed output，或已验证并接入 feed pipeline 的 BYOD。
- 本地 examples 不包含当前价格、涨跌、贡献、事件日期、估值、新闻或基本面事实。

如果数据覆盖、feed 发布、订阅或 push 验证不足，必须降级为 `Lite` 或 `Disabled`，并写清楚证据。不要为了让页面“看起来完整”而编造数据。

## 显式权重规则

如果用户提供权重，必须先校验权重总和。

- 权重总和必须等于 100%。
- 不允许静默归一化。
- `weightedContributionPct = weightPct / 100 * oneDayMovePct`。
- 所有持仓的 `weightedContributionPct` 之和必须等于 summary 中的 `portfolioMovePct`。
- 如果任一资产没有真实价格变动数据，就不能声称 weighted contribution 完整可用。

## 目录结构

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

## 本地验证

运行：

```bash
python3 scripts/validate_portfolio_watch_skill.py --write-report
```

验证覆盖：

- 必要文件和 references 是否存在。
- 触发 / 不触发样例。
- `Full candidate` / `Lite` / `Disabled` 预检。
- Alert quiet / push-candidate 逻辑。
- 本地 prototype 的 fixture 读取。
- README 中的数据来源、隐私和非投资建议边界。
- 公开包脱敏检查，确认不包含私有 dogfood 标识、本机路径、真实 user id、notification id 或生产对象 id。

## 真实 Alva 验证

公开仓库只包含脱敏验证摘要，不包含私有 Alva run artifacts。要声明新的 Full-path 验证，需要在你自己的 Alva namespace 下重新跑完整流程，并记录：

- Alva preflight 和 CLI help 检查。
- Data Skills 覆盖检查。
- 至少两次 feed 或 automation 执行。
- released feed 和 active automation。
- feed-backed Playbook draft / release。
- `alva lint playbook` 结果。
- released Playbook 截图。
- 最新 `runId` 批次隔离和无重复行检查。
- weighted contribution 之和等于 portfolio move。
- README、Remix Guide、Data Health 和 alert sidecar 证据。
- 如已授权公开发布 / 订阅 / 可见 push，则必须限制在 owner 或 test user，并记录 subscription state 与 notification history。

## 当前验证结论

公开包来自三轮 dogfood 后的脱敏版本：

- 第一轮：无权重 watchlist 的真实 `L2/Lite` dogfood。
- 第二轮：显式权重模拟组合的真实 `L2/Lite` dogfood。
- 第三轮：授权 `Full-path` dogfood，覆盖 public release、public visibility、owner-scoped subscription 和 owner-scoped visible push。

当前严格评分：`9.8 / 10`。详细说明见 [docs/QUALITY_SCORE.md](docs/QUALITY_SCORE.md) 和 [docs/VALIDATION_SUMMARY.zh-CN.md](docs/VALIDATION_SUMMARY.zh-CN.md)。

## 公开包边界

这个仓库不包含：

- 私有 Alva 用户名或 namespace。
- 真实 user id。
- 真实 notification id。
- 真实 feed / automation / Playbook id。
- 本机绝对路径。
- secrets、tokens、API keys。
- 真实券商账户或交易数据。

## License

MIT。

