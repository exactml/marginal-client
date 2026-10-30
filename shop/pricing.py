from decimal import ROUND_HALF_UP, Decimal

from shop.catalog import get_item
from shop.models import Order

COUPONS = {"WELCOME10": Decimal("0.10"), "VIP25": Decimal("0.25")}
TAX_RATE = Decimal("0.20")


def subtotal(order: Order) -> Decimal:
    return sum(
        (get_item(line.sku).unit_price * line.quantity for line in order.lines),
        Decimal("0"),
    )


def discount(order: Order, amount: Decimal) -> Decimal:
    rate = COUPONS.get(order.coupon or "", Decimal("0"))
    return amount * rate


def total(order: Order) -> Decimal:
    net = subtotal(order) - discount(order, subtotal(order))
    gross = net * (1 + TAX_RATE)
    # Round once, at the end, half up (money.md).
    return gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
