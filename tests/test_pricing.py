from decimal import Decimal

from shop.models import Order, OrderLine
from shop.pricing import COUPONS, discount, shipping, total


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


def test_discount_never_exceeds_50_percent(monkeypatch):
    monkeypatch.setitem(COUPONS, "HUGE", Decimal("0.90"))
    assert discount(_order("HUGE"), Decimal("100")) == Decimal("50")


def test_shipping_is_free_at_least_100():
    assert shipping(_order()) == Decimal("0")


def test_small_order_pays_the_flat_fee():
    small = Order(customer_id="c-1", lines=[OrderLine(sku="SKU-123", quantity=1)])
    assert shipping(small) == Decimal("4.99")
