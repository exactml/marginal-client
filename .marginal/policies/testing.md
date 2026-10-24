# Testing

- A change to `shop/pricing.py` or `shop/checkout.py` needs a test with the
  worked numbers in a comment, like the existing ones in `tests/test_pricing.py`.
- Don't mock `shop.catalog` or `shop.stock` in tests; they're in-memory already.
