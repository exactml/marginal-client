from decimal import Decimal

from shop.models import Order
from shop.pricing import total
from shop.stock import reserve


def checkout(order: Order) -> Decimal:
    """Reserve stock for each line, then return the amount to charge."""
    for line in order.lines:
        reserve(line.sku, line.quantity)
    return total(order)
