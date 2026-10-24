from decimal import Decimal

from shop.models import Order, OrderLine
from shop.pricing import total


def _order(coupon=None):
    return Order(
        customer_id="c-1",
        lines=[OrderLine(sku="SKU-123", quantity=2), OrderLine(sku="SKU-789", quantity=1)],
        coupon=coupon,
    )


def test_total_adds_tax():
    # (2 * 19.99 + 120.00) * 1.20
    assert total(_order()) == Decimal("191.98")


def test_total_applies_coupon_before_tax():
    # 159.98 * 0.90 * 1.20
    assert total(_order("WELCOME10")) == Decimal("172.78")


def test_unknown_coupon_is_ignored():
    assert total(_order("NOPE")) == total(_order())
