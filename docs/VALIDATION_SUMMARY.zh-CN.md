# Portfolio Watch 公开验证摘要

本仓库是从一次私有三轮 dogfood 中抽取出来的公开脱敏包。仓库不包含私有 owner 名称、user id、notification id、本机路径、带账号上下文的截图或真实生产对象 id。

## 三轮验证历史

1. 无权重 AI leaders watchlist 的 `L2/Lite` dogfood。
   - 已验证真实 Alva feed 执行、active automation、released feed、feed-backed draft Playbook、README、Remix Guide、Data Health、lint、截图、quiet alert sidecar 和最新批次行过滤。
   - 未执行 public release、subscription 或 visible push，因为这些动作需要单独授权。

2. 显式权重模拟组合的 `L2/Lite` dogfood。
   - 已验证 NVDA、MSFT、AAPL、AMZN、META、QQQ 的显式权重。
   - 已验证总权重等于 100%。
   - 已验证来自 Data Skills 的价格变动、weighted contribution、组合加权日变动、benchmark 对比、Data Health 和 contribution 对账。
   - public release 和 visible push 在当轮仍保留为授权后动作。

3. 授权 `Full-path` weighted portfolio dogfood。
   - 已验证本轮只显式触发 `portfolio-watch`。
   - base Alva 文件仅作为平台契约读取，不作为额外用户触发前提。
   - 已创建真实 feed、active automation、released feed、feed-backed Playbook、public release、public visibility、owner-scoped subscription 和 owner-scoped visible push 验证。
   - 已验证最新 `runId` 批次隔离、无重复行、weighted contribution 之和等于 portfolio move。
   - 已验证 `alva lint playbook` 为 0 errors、0 warnings、0 info。

## 当前质量判断

当前严格评分：`9.8 / 10`。

核心工作流已经通过真实 Full-path 验证。剩余差距主要不是流程本身，而是更广资产与分发场景的覆盖：

- 当前真实 dogfood 主要覆盖 US equity / ETF portfolio，还没有覆盖非美股、crypto、混合资产或 BYOD 变体。
- 有一个平台形态需要后续 Agent 注意：Playbook subscription cascade 后，delivery history 可能记录在 feed-scoped notification history，而不是 playbook-scoped history。

## 公开边界

本仓库不包含：

- 私有 Alva 用户名或 owner namespace。
- 真实 user id。
- 真实 notification id。
- 真实 feed、automation 或 Playbook id。
- 本机绝对路径。
- secrets、tokens、API keys 或券商数据。
- 交易执行示例。

公开包的目标是帮助 Agent 在使用者自己的 Alva namespace 下构建安全的 Portfolio Watch 工作流。

