_STOCK = {"SKU-123": 10, "SKU-456": 0, "SKU-789": 3}
# Sold before they arrive: these may be reserved past what's on hand.
PREORDER = {"SKU-789"}


class OutOfStock(Exception):
    pass


def available(sku: str) -> int:
    return _STOCK.get(sku, 0)


def reserve(sku: str, quantity: int) -> None:
    if sku not in PREORDER and available(sku) < quantity:
        raise OutOfStock(f"{sku}: wanted {quantity}, have {available(sku)}")
    _STOCK[sku] -= quantity
