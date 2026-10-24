_STOCK = {"SKU-123": 10, "SKU-456": 0, "SKU-789": 3}


class OutOfStock(Exception):
    pass


def available(sku: str) -> int:
    return _STOCK.get(sku, 0)


def reserve(sku: str, quantity: int) -> None:
    if available(sku) < quantity:
        raise OutOfStock(f"{sku}: wanted {quantity}, have {available(sku)}")
    _STOCK[sku] -= quantity
