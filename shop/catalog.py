from decimal import Decimal

from shop.models import Item

_CATALOG = {
    "SKU-123": Item(sku="SKU-123", unit_price=Decimal("19.99")),
    "SKU-456": Item(sku="SKU-456", unit_price=Decimal("5.00")),
    "SKU-789": Item(sku="SKU-789", unit_price=Decimal("120.00")),
}


class UnknownSku(KeyError):
    pass


def get_item(sku: str) -> Item:
    try:
        return _CATALOG[sku]
    except KeyError:
        raise UnknownSku(sku) from None
