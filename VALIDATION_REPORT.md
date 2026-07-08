# Portfolio Watch Skill 本地结构验证报告

生成方式：`scripts/validate_portfolio_watch_skill.py --write-report`。

> 本脚本只验证公开 Skill 包、样例配置、本地原型、脱敏状态和逻辑检查；它不调用 Alva 平台，也不能替代使用者自己 namespace 下的真实 dogfood 复验。

## 结论

- 通过：49
- 失败：0
- 真实 Alva dogfood：公开仓库只保留脱敏摘要，见 `docs/VALIDATION_SUMMARY.md`；使用者需要在自己的 Alva namespace 下重新跑真实验证。
- 数据边界：本地原型不包含当前价格、涨跌、贡献、事件日期、估值、新闻或基本面数值。

## 检查明细

- `PASS` exists:SKILL.md: SKILL.md
- `PASS` exists:README.md: README.md
- `PASS` exists:README.zh-CN.md: README.zh-CN.md
- `PASS` exists:LICENSE: LICENSE
- `PASS` exists:.gitignore: .gitignore
- `PASS` exists:docs/VALIDATION_SUMMARY.md: docs/VALIDATION_SUMMARY.md
- `PASS` exists:docs/VALIDATION_SUMMARY.zh-CN.md: docs/VALIDATION_SUMMARY.zh-CN.md
- `PASS` exists:docs/QUALITY_SCORE.md: docs/QUALITY_SCORE.md
- `PASS` exists:references/request-routing.md: references/request-routing.md
- `PASS` exists:references/requirement-extraction.md: references/requirement-extraction.md
- `PASS` exists:references/data-preflight.md: references/data-preflight.md
- `PASS` exists:references/playbook-build.md: references/playbook-build.md
- `PASS` exists:references/alert-policy.md: references/alert-policy.md
- `PASS` exists:references/validation-checklist.md: references/validation-checklist.md
- `PASS` exists:portfolio-watch.config.json: portfolio-watch.config.json
- `PASS` exists:examples/no-weight-watchlist.config.json: examples/no-weight-watchlist.config.json
- `PASS` exists:examples/abnormal-portfolio.config.json: examples/abnormal-portfolio.config.json
- `PASS` exists:examples/portfolio-watch-playbook/index.html: examples/portfolio-watch-playbook/index.html
- `PASS` exists:examples/portfolio-watch-playbook/README.md: examples/portfolio-watch-playbook/README.md
- `PASS` exists:examples/portfolio-watch-playbook/portfolio-watch-sample-feed.json: examples/portfolio-watch-playbook/portfolio-watch-sample-feed.json
- `PASS` exists:examples/portfolio-watch-playbook/browser-verification.json: examples/portfolio-watch-playbook/browser-verification.json
- `PASS` exists:examples/portfolio-watch-playbook/prototype-screenshot.png: examples/portfolio-watch-playbook/prototype-screenshot.png
- `PASS` exists:scripts/validate_portfolio_watch_skill.py: scripts/validate_portfolio_watch_skill.py
- `PASS` skill:no_todo: SKILL.md contains no template TODO
- `PASS` skill:frontmatter: frontmatter name present
- `PASS` route:帮我把 NVDA/MSFT/AAPL: expected=trigger; actual=trigger
- `PASS` route:我有一组持仓，想每天看贡献和风险，异: expected=trigger; actual=trigger
- `PASS` route:做一个可分享的 AI leaders: expected=trigger; actual=trigger
- `PASS` route:NVDA 现在怎么看？: expected=no_trigger; actual=no_trigger
- `PASS` route:监控 CPI 和 FOMC，突破时提: expected=no_trigger; actual=no_trigger
- `PASS` route:回测一个组合再平衡策略: expected=no_trigger; actual=no_trigger
- `PASS` route:连接我的券商账户并自动调仓: expected=no_trigger; actual=no_trigger
- `PASS` preflight:portfolio-watch.config.json: expected=Full candidate; actual=Full candidate; issues=requires_live_Data_Skills_feed_release_and_alert_verification_for_Full
- `PASS` preflight:no-weight-watchlist.config.json: expected=Lite; actual=Lite; issues=contribution_disabled_until_weights_or_equal_weight_confirmed
- `PASS` preflight:abnormal-portfolio.config.json: expected=Disabled; actual=Disabled; issues=duplicate:NVDA, invalid:BADTICKER123, mvp_coverage_gap:0700.HK:HK:stock, mvp_coverage_gap:BTC:GLOBAL:crypto
- `PASS` alert:calm_quiet: quiet; <|SKIP_NOTIFICATION|>
- `PASS` alert:material_push: push_candidate; Portfolio Watch material change detected. Not investment advice.
- `PASS` alert:stale_suppressed: quiet; <|SKIP_NOTIFICATION|>
- `PASS` alert:cooldown_suppressed: quiet; <|SKIP_NOTIFICATION|>
- `PASS` alert:weak_evidence_suppressed: quiet; <|SKIP_NOTIFICATION|>
- `PASS` page:runtime_fixture_read: HTML reads fixture at runtime
- `PASS` page:no_market_values_in_fixture: fixture market values are null and explicitly disabled
- `PASS` page:quiet_alert_fixture: fixture alert is quiet
- `PASS` browser:desktop_render: desktop render has 6 rows, Disabled mode, quiet alert
- `PASS` browser:mobile_no_horizontal_overflow: mobile render has 6 rows and no horizontal overflow
- `PASS` browser:no_console_errors: system Chromium console errors empty
- `PASS` readme:root_boundaries: root README includes provenance, privacy, and advisory boundaries
- `PASS` readme:prototype_boundaries: prototype README states no live values and no advice
- `PASS` public:no_private_dogfood_identifiers: no private dogfood ids/usernames/absolute paths found

## 剩余风险

- 本地结构验证不能证明真实 Alva Data Skills、feed fresh run、release、lint、截图和 sidecar；这些必须由使用者在自己的账号下重新验证。
- Push 本地逻辑验证不能证明真实订阅或可见 push delivery；公开包只描述授权边界和复验方法。
- 本地原型用 fixture 证明页面读取与 Disabled 状态，不证明市场数据覆盖。

## 下一步

1. 在安装了 Alva base skill 和 Alva CLI 的环境中，按 `SKILL.md` 完成真实 feed / Playbook / alert dogfood。
2. 未获公开发布、订阅或可见 push 授权时，保持 `L2/Lite`；获得明确授权后必须限制为本人/测试对象并记录 notification history。
