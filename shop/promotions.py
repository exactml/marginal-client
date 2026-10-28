from decimal import Decimal


def apply_discount(price: Decimal, percent: int) -> Decimal:
    """The price after a `percent` discount, where `percent` is 0-100."""
    return price - price * percent
