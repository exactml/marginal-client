from decimal import Decimal

from pydantic import BaseModel, Field


class Item(BaseModel):
    sku: str
    unit_price: Decimal = Field(ge=0)


class OrderLine(BaseModel):
    sku: str
    quantity: int = Field(gt=0)


class Order(BaseModel):
    customer_id: str
    lines: list[OrderLine]
    coupon: str | None = None
