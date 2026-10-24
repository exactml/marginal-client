import pytest

from shop.checkout import checkout
from shop.models import Order, OrderLine
from shop.stock import OutOfStock


def test_checkout_rejects_an_out_of_stock_line():
    order = Order(customer_id="c-1", lines=[OrderLine(sku="SKU-456", quantity=1)])

    with pytest.raises(OutOfStock):
        checkout(order)
