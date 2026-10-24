# marginal-client

An end-to-end test customer for [marginal](https://github.com/exactml/marginal).
It's a small order-pricing app (`shop/`) with marginal installed exactly as
the README tells a new user to: `marginal init` from PyPI, a reviewer model,
two policies, and the `exactml/marginal-action@v1` workflow.

Unit tests in marginal mock GitHub and the model. This repo is where a
change gets seen the way a team sees it: on a real PR, with a real review.

## The app

```text
shop/checkout.py  -> reserves stock, then charges pricing.total()
shop/pricing.py   -> subtotal, coupon discount, 20% tax, rounding
shop/catalog.py   -> SKU -> unit price
shop/stock.py     -> SKU -> units on hand
```

Example: 2 × `SKU-123` (19.99) + 1 × `SKU-789` (120.00) with coupon
`WELCOME10` charges `159.98 × 0.90 × 1.20 = 172.78`.

```bash
uv run pytest
```

## Release checklist

Before cutting a marginal release, open each PR below against `master`
(one branch per scenario, then close it unmerged) and check the result.

| # | Scenario | How | Expect |
|---|---|---|---|
| 1 | Real bug | Change `ROUND_HALF_UP` to `ROUND_DOWN`, or make a price a `float` | An inline finding on the changed line; `money.md` cited |
| 2 | Out-of-diff caller | Change `pricing.total`'s signature without touching `checkout.py` | A finding that names the caller in `checkout.py` |
| 3 | Clean PR | Fix a docstring typo | `✅ No issues found`, no inline comments |
| 4 | Fix after a finding | Push a fix to scenario 1's branch | The thread gets a `✅ Resolved` reply and is collapsed |
| 5 | Disputed finding | Reply to a finding explaining why it's wrong | Next push closes it, crediting you |
| 6 | Lockfile-only change | `uv lock --upgrade-package pydantic` | No model call; `1 file(s) not reviewed` |
| 7 | Draft PR | Open any change as a draft | No review; marking it ready triggers one |
| 8 | Opt-out label | Add the `skip-review` label, then push | No review on that push |

Scenarios 6–8 need marginal ≥ 0.2.9.

## Setup notes

Friction found while installing marginal here, to fix in marginal's docs:

- There's no `marginal --version` (it exits 2 with a usage error), so
  there's no quick way to confirm which release `uvx`/`pip` installed.
