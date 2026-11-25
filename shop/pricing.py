from decimal import ROUND_DOWN, Decimal

from shop.catalog import get_item
from shop.models import Order

COUPONS = {"WELCOME10": Decimal("0.10"), "VIP25": Decimal("0.25")}
TAX_RATE = Decimal("0.20")
# Finance caps any coupon at 50% so a stacked promotion can never make an order free.
MAX_DISCOUNT_RATE = Decimal("0.50")
# Orders of 100 or more ship free; below that a flat fee applies.
FREE_SHIPPING_MIN = Decimal("100")
SHIPPING_FEE = Decimal("4.99")


def subtotal(order: Order) -> Decimal:
    return sum(
        (get_item(line.sku).unit_price * line.quantity for line in order.lines),
        Decimal("0"),
    )


def discount(order: Order, amount: Decimal) -> Decimal:
    rate = COUPONS.get(order.coupon or "", Decimal("0"))
    return amount * min(rate, MAX_DISCOUNT_RATE)


def shipping(order: Order) -> Decimal:
    # The threshold uses the subtotal before any coupon.
    return Decimal("0") if subtotal(order) >= FREE_SHIPPING_MIN else SHIPPING_FEE


def total(order: Order) -> Decimal:
    net = subtotal(order) - discount(order, subtotal(order))
    gross = net * (1 + TAX_RATE)
    return gross.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
