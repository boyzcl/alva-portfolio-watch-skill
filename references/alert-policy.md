# Alert Policy

Portfolio Watch alerts are low-noise by default. They should help users notice material changes without turning every daily refresh into a notification.

## Decision Order

1. Check data health. If core data is stale, missing, or weak, suppress visible push.
2. Check cooldown. If the same rule already fired within `cooldownHours`, suppress.
3. Check materiality thresholds.
4. Check evidence strength. A weak event clue or isolated headline cannot be the sole reason for a push.
5. Emit either a push message or a quiet sidecar record.

## Default Rules

| Rule | Default |
| --- | --- |
| Single-symbol move | Push only if absolute move is at or above configured material threshold and data is fresh. |
| Portfolio move | Push only if portfolio-level move is material and contribution can be computed or watchlist mode copy is clear. |
| Event window | Push only for verified upcoming/recent events inside the configured window when the user enabled event alerts. |
| Stale data | Always suppress push. |
| Weak evidence | Suppress or mark as context-only. |
| Calm day | Emit `<|SKIP_NOTIFICATION|>`. |

## Sidecar Shape

Use `notify/message` for Portfolio Watch messages unless the user explicitly needs a trading signal target. A quiet run writes:

```text
<|SKIP_NOTIFICATION|>
```

A visible push message must include:

- Portfolio/watchlist name.
- Trigger type and rule.
- Relevant symbols.
- Data freshness.
- Non-advisory wording.

It must not include buy/sell language, target prices, position sizing, rebalancing instructions, or execution instructions.

## Verification Scenarios

Validate at least:

1. Calm run: no material change -> `<|SKIP_NOTIFICATION|>`.
2. Material run: fresh data and threshold breached -> push candidate.
3. Stale run: threshold breached but stale data -> suppressed.
4. Cooldown run: repeated trigger inside cooldown -> suppressed.

If real Alva push is configured, verify sidecar exists, feed is released after sidecar addition, publisher has `--push-notify`, subscription exists, and a real run writes a fresh sidecar record.

For authorized dogfood of visible delivery, use verification/observation copy
only and keep the subscriber target to the owner or explicit test subject. A
one-shot verification push may be followed by later quiet runs; validate both
facts separately:

- the visible verification body exists in `notify/message` and notification
  history with `status=sent`;
- the latest run still reconciles normally and may return
  `<|SKIP_NOTIFICATION|>` after the one-shot verification is consumed.
