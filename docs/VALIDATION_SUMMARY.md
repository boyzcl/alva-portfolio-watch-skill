# Portfolio Watch Public Validation Summary

This repository is a sanitized public package extracted from a private
three-round dogfood process. Private owner names, user ids, notification ids,
local paths, screenshots with account context, and production object ids are
not included.

## Validation History

1. `L2/Lite` dogfood for an unweighted AI leaders watchlist.
   - Verified real Alva feed execution, active automation, released feed,
     feed-backed draft Playbook, README, Remix Guide, Data Health, lint,
     screenshot, quiet alert sidecar, and latest-batch row filtering.
   - Did not perform public release, subscription, or visible push because
     those require explicit authorization.

2. `L2/Lite` dogfood for a weighted simulated portfolio.
   - Verified explicit weights for NVDA, MSFT, AAPL, AMZN, META, and QQQ.
   - Verified total weight equals 100%.
   - Verified Data Skills-backed price move, weighted contribution, portfolio
     weighted daily move, benchmark comparison, Data Health, and contribution
     reconciliation.
   - Kept public release and visible push out of scope pending authorization.

3. Authorized `Full-path` dogfood for a weighted simulated portfolio.
   - Verified that only `portfolio-watch` was explicitly triggered.
   - Read base Alva platform contracts only as implementation dependencies,
     not as an extra user trigger requirement.
   - Created real feed, active automation, released feed, feed-backed
     Playbook, public release, public visibility, owner-scoped subscription,
     and owner-scoped visible push verification.
   - Verified latest `runId` batch isolation, no duplicate rows, and weighted
     contribution sum equal to portfolio move.
   - Verified `alva lint playbook` passed with 0 errors, 0 warnings, 0 info.

## Current Quality Judgment

Current strict score: `9.8 / 10`.

The remaining gap is not the core workflow. It is broader coverage:

- Public dogfood has covered US equity/ETF portfolios, not non-US equities,
  crypto, mixed-asset portfolios, or BYOD variants.
- One platform-specific gotcha remains: Playbook subscription delivery may be
  recorded in feed-scoped notification history after subscription cascade.

## Public Boundary

This repository does not include:

- Private Alva usernames or owner namespace.
- Real user ids.
- Real notification ids.
- Real feed, automation, or Playbook ids.
- Local absolute filesystem paths.
- Secrets, tokens, API keys, or brokerage data.
- Trading execution examples.

The public package is intended to help agents build safe Portfolio Watch
workflows in the user's own Alva namespace.

