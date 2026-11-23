from decimal import Decimal

from shop.models import Order
from shop.pricing import total
from shop.stock import available, reserve


def checkout(order: Order) -> Decimal:
    """Reserve stock for every line, then return the amount to charge."""
    for line in order.lines:
        if line.quantity > available(line.sku):
            raise ValueError(f"{line.sku}: only {available(line.sku)} left")
    for line in order.lines:
        reserve(line.sku, line.quantity)
    return total(order)
