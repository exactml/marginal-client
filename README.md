# marginal-client

An end-to-end test customer for [marginal](https://github.com/exactml/marginal).
It's a small order-pricing app (`shop/`) set up the way marginal's README
tells a new user to (`marginal init`, a reviewer model, two policies), with
one difference: the workflow installs marginal **from git** (`master` by
default) instead of from PyPI. So a change is tested here as soon as it
merges, without waiting for a release. The released `marginal-action@v1` path
is exercised by marginal's own repo on every PR.

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
Every PR here is reviewed with marginal's current `master`.

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

## Testing an unmerged marginal branch

To check a marginal PR before it merges, open the matching scenario PR here,
then review it with that branch:

```bash
gh workflow run marginal.yml -R exactml/marginal-client -f ref=<marginal-branch> -f pr=<PR number here>
```

The run log's first line names the ref it installed. This is the e2e step of
marginal's `prove-it` skill. It needs write access to this repo, so outside
contributors leave it to a maintainer.

## Setup notes

Friction found while installing marginal here, to fix in marginal's docs:

- There was no `marginal --version` (fixed in exactml/marginal#145).
- `gh secret set` run without a terminal saves an empty secret, and the
  error said the key wasn't set (clearer message in exactml/marginal#144).
