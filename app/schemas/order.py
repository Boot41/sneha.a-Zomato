# app/schemas/order.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    placed = "placed"
    delivered = "delivered"

class PaymentStatus(str, Enum):
    paid = "Paid"
    unpaid = "Unpaid"

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_id: int
    restaurant_id: int
    total_price: float
    payment_status: PaymentStatus = PaymentStatus.unpaid
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: OrderStatus

class OrderItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    total_price: float
    status: OrderStatus
    payment_status: PaymentStatus
    created_at: datetime
    restaurant_name: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class OrderItemSummary(BaseModel):
    id: int
    menu_item_id: int
    name: str
    price: float
    quantity: int

class OrderSummary(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    total_price: float
    status: str
    payment_status: str
    created_at: datetime
    restaurant_name: str
    items: List[OrderItemSummary]

    class Config:
        from_attributes = True