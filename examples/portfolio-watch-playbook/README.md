# AI Leaders Portfolio Watch Prototype

这个目录是由 `portfolio-watch` Skill 生成的本地 Playbook 原型，用于验证页面结构、运行时数据读取、Data Health、Alert quiet 状态和边界文案。

## 当前状态

- 模式：`Disabled` local prototype。
- 数据：只读取 `portfolio-watch-sample-feed.json`，该 fixture 不包含任何当前价格、涨跌、贡献、财报日期、估值、新闻或基本面数值。
- 用途：验证 UI 和流程，不验证市场事实。
- 真实发布：未执行。

## 数据与来源

真实 Alva Playbook 必须从 Data Skills、released feed output 或 validated BYOD 读取金融值。页面不能把当前价格、涨跌、贡献、事件日期、估值或新闻事实写死在 HTML 或 README 中。

当前 prototype 中可见的权重来自示例配置 `portfolio-watch.config.json`，是 public template 示例，不代表真实持仓或投资建议。

## Alert

当前 fixture 的 `notify/message` 为：

```text
<|SKIP_NOTIFICATION|>
```

原因是本地 prototype 没有 live Data Skills/feed 运行。真实提醒只有在数据 fresh、阈值触发、证据足够、cooldown 通过且 sidecar/subscription 验证后才能声明完成。

## Remix

替换组合时可以改：

- `portfolioName`
- `symbols`
- `weightPct` 或 `watchlist_only`
- `benchmark`
- `alertRules`
- `visibilityIntent`

必须保留：

- provenance / Data Health
- Full / Lite / Disabled 降级
- quiet-first alert policy
- 非投资建议边界
- 不硬编码金融值

## 边界

本原型不提供买卖建议、目标价、仓位建议、调仓建议或交易执行，也不接入真实账户。
