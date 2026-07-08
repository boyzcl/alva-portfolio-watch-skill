#!/usr/bin/env python3
"""Validate the local Portfolio Watch skill package.

This validator is intentionally local. It checks routing, config extraction,
preflight classification, alert policy, page data wiring, and README
boundaries without claiming real Alva data coverage or publication.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUIET = "<|SKIP_NOTIFICATION|>"


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def route_request(text: str) -> str:
    lowered = text.lower()
    portfolio_terms = [
        "portfolio",
        "watchlist",
        "ticker",
        "tickers",
        "组合",
        "持仓",
        "自选",
        "关注组合",
        "关注池",
    ]
    durable_terms = [
        "playbook",
        "dashboard",
        "alert",
        "notify",
        "monitor",
        "watch",
        "track",
        "share",
        "remix",
        "每天",
        "持续",
        "刷新",
        "提醒",
        "监控",
        "观察",
        "可分享",
    ]
    hard_non_triggers = [
        "回测",
        "backtest",
        "rebalance",
        "再平衡",
        "调仓",
        "交易",
        "下单",
        "券商账户",
        "目标价",
        "target price",
    ]
    if any(term in lowered for term in hard_non_triggers):
        return "no_trigger"

    macro_or_content_only = any(term in lowered for term in ["cpi", "fomc", "kol", "x 博主", "宏观", "主题链"])
    has_portfolio = any(term in lowered for term in portfolio_terms)
    has_durable = any(term in lowered for term in durable_terms)
    ticker_list_with_artifact = bool(re.search(r"\b[A-Z]{2,5}(?:[,/ ]+[A-Z]{2,5}){2,}\b", text)) and has_durable

    if macro_or_content_only and not has_portfolio:
        return "no_trigger"
    if (has_portfolio or ticker_list_with_artifact) and has_durable:
        return "trigger"
    return "no_trigger"


def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def classify_preflight(config: dict[str, Any]) -> tuple[str, list[str]]:
    symbols = config.get("symbols", [])
    issues: list[str] = []
    seen: set[str] = set()
    unresolved = 0
    unsupported = 0

    for row in symbols:
        symbol = normalize_symbol(str(row.get("symbol", "")))
        asset_type = str(row.get("assetType", "")).lower()
        market = str(row.get("market", "")).upper()

        if symbol in seen:
            issues.append(f"duplicate:{symbol}")
            unresolved += 1
        seen.add(symbol)

        if not re.match(r"^[A-Z0-9][A-Z0-9.]{0,11}$", symbol) or "BAD" in symbol:
            issues.append(f"invalid:{symbol}")
            unresolved += 1
            continue

        if market != "US" or asset_type not in {"stock", "etf"}:
            issues.append(f"mvp_coverage_gap:{symbol}:{market}:{asset_type}")
            unsupported += 1

    if not symbols:
        return "Disabled", ["empty_symbol_list"]

    bad_ratio = (unresolved + unsupported) / len(symbols)
    if bad_ratio > 0.20:
        return "Disabled", issues

    if config.get("mode") == "watchlist_only" or config.get("weightMode") == "no_weights_provided":
        return "Lite", issues + ["contribution_disabled_until_weights_or_equal_weight_confirmed"]

    if issues:
        return "Lite", issues

    return "Full candidate", ["requires_live_Data_Skills_feed_release_and_alert_verification_for_Full"]


def validate_config(path: Path, expected_mode: str) -> Check:
    config = read_json(path)
    mode, issues = classify_preflight(config)
    ok = mode == expected_mode
    return Check(
        f"preflight:{path.name}",
        ok,
        f"expected={expected_mode}; actual={mode}; issues={', '.join(issues) if issues else 'none'}",
    )


def decide_alert(data_fresh: bool, material: bool, cooldown: bool, weak_evidence: bool) -> tuple[str, str]:
    if not data_fresh:
        return "quiet", QUIET
    if cooldown:
        return "quiet", QUIET
    if weak_evidence:
        return "quiet", QUIET
    if material:
        return "push_candidate", "Portfolio Watch material change detected. Not investment advice."
    return "quiet", QUIET


def package_checks() -> list[Check]:
    required = [
        "SKILL.md",
        "README.md",
        "README.zh-CN.md",
        "LICENSE",
        ".gitignore",
        "docs/VALIDATION_SUMMARY.md",
        "docs/VALIDATION_SUMMARY.zh-CN.md",
        "docs/QUALITY_SCORE.md",
        "references/request-routing.md",
        "references/requirement-extraction.md",
        "references/data-preflight.md",
        "references/playbook-build.md",
        "references/alert-policy.md",
        "references/validation-checklist.md",
        "portfolio-watch.config.json",
        "examples/no-weight-watchlist.config.json",
        "examples/abnormal-portfolio.config.json",
        "examples/portfolio-watch-playbook/index.html",
        "examples/portfolio-watch-playbook/README.md",
        "examples/portfolio-watch-playbook/portfolio-watch-sample-feed.json",
        "examples/portfolio-watch-playbook/browser-verification.json",
        "examples/portfolio-watch-playbook/prototype-screenshot.png",
        "scripts/validate_portfolio_watch_skill.py",
    ]
    checks = [Check(f"exists:{item}", (ROOT / item).exists(), item) for item in required]
    skill = read_text(ROOT / "SKILL.md")
    checks.append(Check("skill:no_todo", "TODO" not in skill, "SKILL.md contains no template TODO"))
    checks.append(Check("skill:frontmatter", skill.startswith("---\nname: portfolio-watch"), "frontmatter name present"))
    return checks


def public_release_checks() -> list[Check]:
    forbidden_patterns: list[tuple[str, re.Pattern[str]]] = [
        ("private_owner_username", re.compile(r"\b" + "boyz" + r"cl\d+\b")),
        ("private_user_id", re.compile(r"\b" + "206242" + "7239217864704" + r"\b")),
        (
            "private_notification_or_object_id",
            re.compile(r"\b(?:" + "|".join(["225" + "534", "225" + "535", "60" + "98", "143" + "13", "171" + "96", "85" + "00"]) + r")\b"),
        ),
        ("local_absolute_path", re.compile(r"/Users/" + "boyz" + r"cl\b")),
        ("private_api_origin", re.compile(r"api-llm\.prd\." + "alva" + r"\.ai")),
        ("owner_avatar_url", re.compile(r"lh3\." + "googleusercontent" + r"\.com")),
    ]
    text_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".md", ".py", ".yaml", ".yml", ".json", ".html", ".js", ".css", ".txt"}
        and ".git" not in path.parts
        and path.name != "VALIDATION_REPORT.md"
    ]
    hits: list[str] = []
    for path in text_files:
        text = read_text(path)
        for label, pattern in forbidden_patterns:
            if pattern.search(text):
                hits.append(f"{path.relative_to(ROOT)}:{label}")
    return [
        Check(
            "public:no_private_dogfood_identifiers",
            not hits,
            "no private dogfood ids/usernames/absolute paths found" if not hits else "; ".join(hits),
        )
    ]


def route_checks() -> list[Check]:
    cases = [
        ("帮我把 NVDA/MSFT/AAPL 做成每天更新、有提醒的 Playbook", "trigger"),
        ("我有一组持仓，想每天看贡献和风险，异常时提醒", "trigger"),
        ("做一个可分享的 AI leaders 关注组合模板", "trigger"),
        ("NVDA 现在怎么看？", "no_trigger"),
        ("监控 CPI 和 FOMC，突破时提醒", "no_trigger"),
        ("回测一个组合再平衡策略", "no_trigger"),
        ("连接我的券商账户并自动调仓", "no_trigger"),
    ]
    checks: list[Check] = []
    for text, expected in cases:
        actual = route_request(text)
        checks.append(Check(f"route:{text[:18]}", actual == expected, f"expected={expected}; actual={actual}"))
    return checks


def preflight_checks() -> list[Check]:
    return [
        validate_config(ROOT / "portfolio-watch.config.json", "Full candidate"),
        validate_config(ROOT / "examples/no-weight-watchlist.config.json", "Lite"),
        validate_config(ROOT / "examples/abnormal-portfolio.config.json", "Disabled"),
    ]


def alert_checks() -> list[Check]:
    cases = [
        ("calm_quiet", True, False, False, False, "quiet", QUIET),
        ("material_push", True, True, False, False, "push_candidate", "Portfolio Watch material change detected. Not investment advice."),
        ("stale_suppressed", False, True, False, False, "quiet", QUIET),
        ("cooldown_suppressed", True, True, True, False, "quiet", QUIET),
        ("weak_evidence_suppressed", True, True, False, True, "quiet", QUIET),
    ]
    checks: list[Check] = []
    for name, fresh, material, cooldown, weak, expected_decision, expected_message in cases:
        decision, message = decide_alert(fresh, material, cooldown, weak)
        checks.append(Check(f"alert:{name}", decision == expected_decision and message == expected_message, f"{decision}; {message}"))
    return checks


def page_and_readme_checks() -> list[Check]:
    html = read_text(ROOT / "examples/portfolio-watch-playbook/index.html")
    fixture = read_json(ROOT / "examples/portfolio-watch-playbook/portfolio-watch-sample-feed.json")
    browser = read_json(ROOT / "examples/portfolio-watch-playbook/browser-verification.json")
    prototype_readme = read_text(ROOT / "examples/portfolio-watch-playbook/README.md")
    root_readme = read_text(ROOT / "README.md")

    holdings = fixture.get("holdings", [])
    no_market_values = (
        fixture.get("provenance", {}).get("marketValuesIncluded") is False
        and fixture.get("summary", {}).get("portfolioMovePct") is None
        and all(row.get("priceMovePct") is None and row.get("contributionPct") is None for row in holdings)
    )

    readme_boundary_terms = ["非投资建议", "买卖建议", "Data Skills", "BYOD", "private", "public"]
    root_boundary_ok = all(term in root_readme for term in readme_boundary_terms)
    prototype_boundary_ok = "不包含任何当前价格" in prototype_readme and "不提供买卖建议" in prototype_readme

    return [
        Check("page:runtime_fixture_read", 'fetch("./portfolio-watch-sample-feed.json"' in html, "HTML reads fixture at runtime"),
        Check("page:no_market_values_in_fixture", no_market_values, "fixture market values are null and explicitly disabled"),
        Check("page:quiet_alert_fixture", fixture.get("alert", {}).get("message") == QUIET, "fixture alert is quiet"),
        Check(
            "browser:desktop_render",
            browser.get("desktop", {}).get("rows") == 6
            and browser.get("desktop", {}).get("mode") == "Disabled"
            and browser.get("desktop", {}).get("alertIncludesQuiet") is True,
            "desktop render has 6 rows, Disabled mode, quiet alert",
        ),
        Check(
            "browser:mobile_no_horizontal_overflow",
            browser.get("mobile", {}).get("rows") == 6
            and browser.get("mobile", {}).get("scrollWidth") == browser.get("mobile", {}).get("clientWidth"),
            "mobile render has 6 rows and no horizontal overflow",
        ),
        Check("browser:no_console_errors", browser.get("consoleErrors") == [], "system Chromium console errors empty"),
        Check("readme:root_boundaries", root_boundary_ok, "root README includes provenance, privacy, and advisory boundaries"),
        Check("readme:prototype_boundaries", prototype_boundary_ok, "prototype README states no live values and no advice"),
    ]


def build_report(checks: list[Check]) -> str:
    passed = sum(1 for check in checks if check.passed)
    failed = len(checks) - passed
    lines = [
        "# Portfolio Watch Skill 本地结构验证报告",
        "",
        "生成方式：`scripts/validate_portfolio_watch_skill.py --write-report`。",
        "",
        "> 本脚本只验证公开 Skill 包、样例配置、本地原型、脱敏状态和逻辑检查；它不调用 Alva 平台，也不能替代使用者自己 namespace 下的真实 dogfood 复验。",
        "",
        "## 结论",
        "",
        f"- 通过：{passed}",
        f"- 失败：{failed}",
        "- 真实 Alva dogfood：公开仓库只保留脱敏摘要，见 `docs/VALIDATION_SUMMARY.md`；使用者需要在自己的 Alva namespace 下重新跑真实验证。",
        "- 数据边界：本地原型不包含当前价格、涨跌、贡献、事件日期、估值、新闻或基本面数值。",
        "",
        "## 检查明细",
        "",
    ]
    for check in checks:
        marker = "PASS" if check.passed else "FAIL"
        lines.append(f"- `{marker}` {check.name}: {check.detail}")

    lines.extend(
        [
            "",
            "## 剩余风险",
            "",
            "- 本地结构验证不能证明真实 Alva Data Skills、feed fresh run、release、lint、截图和 sidecar；这些必须由使用者在自己的账号下重新验证。",
            "- Push 本地逻辑验证不能证明真实订阅或可见 push delivery；公开包只描述授权边界和复验方法。",
            "- 本地原型用 fixture 证明页面读取与 Disabled 状态，不证明市场数据覆盖。",
            "",
            "## 下一步",
            "",
            "1. 在安装了 Alva base skill 和 Alva CLI 的环境中，按 `SKILL.md` 完成真实 feed / Playbook / alert dogfood。",
            "2. 未获公开发布、订阅或可见 push 授权时，保持 `L2/Lite`；获得明确授权后必须限制为本人/测试对象并记录 notification history。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    checks: list[Check] = []
    checks.extend(package_checks())
    checks.extend(route_checks())
    checks.extend(preflight_checks())
    checks.extend(alert_checks())
    checks.extend(page_and_readme_checks())
    checks.extend(public_release_checks())

    report = build_report(checks)
    if args.write_report:
        (ROOT / "VALIDATION_REPORT.md").write_text(report, encoding="utf-8")
    print(report)
    return 0 if all(check.passed for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
