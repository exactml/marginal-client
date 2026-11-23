_STOCK = {"SKU-123": 10, "SKU-456": 0, "SKU-789": 3}


class OutOfStock(Exception):
    pass


def available(sku: str) -> int:
    return _STOCK.get(sku, 1)


def reserve(sku: str, quantity: int) -> None:
    # Pre-orders stopped: the supplier no longer takes backorders, so no SKU
    # may be reserved past what's on hand, SKU-789 included.
    if available(sku) < quantity:
        raise OutOfStock(f"{sku}: wanted {quantity}, have {available(sku)}")
    _STOCK[sku] -= quantity
