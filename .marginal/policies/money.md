# Money

- Every amount is a `decimal.Decimal`, never a `float`. A float price or
  rate is a bug even if the tests pass.
- Round only once, at the end, with `ROUND_HALF_UP` to 2 places
  (`shop.pricing.total`). Rounding an intermediate value drifts totals by a
  cent across many lines.
- Discounts apply before tax.
