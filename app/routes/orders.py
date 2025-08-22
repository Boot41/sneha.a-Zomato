# app/routes/orders.py
from fastapi import APIRouter, HTTPException
from app.models import orders
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderSummary, OrderItemSummary
from typing import List
from app.database import get_db

router = APIRouter(
    tags=["Orders"]
)

# ✅ Create a new order
@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate):
    order_items_data = [item.dict() for item in order.items]
    # Use getattr to safely get payment_status with a default value
    payment_status = getattr(order, 'payment_status', None)
    payment_status_value = payment_status.value if payment_status else 'Unpaid'
    
    new_order = orders.create_order(
        customer_id=order.customer_id,
        restaurant_id=order.restaurant_id,
        total_price=order.total_price,
        items=order_items_data,
        payment_status=payment_status_value
    )
    if not new_order:
        raise HTTPException(status_code=400, detail="Order could not be created")
    # Manually cast Decimal types to float for Pydantic validation
    new_order['total_price'] = float(new_order['total_price'])
    for item in new_order['items']:
        item['price'] = float(item['price'])

    return OrderResponse(**new_order)


# ✅ Get order by ID
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    conn = get_db()
    cur = conn.cursor()
    try:
        order = orders.get_order_by_id(cur, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Manually cast Decimal types to float for Pydantic validation
        order['total_price'] = float(order['total_price'])
        for item in order['items']:
            item['price'] = float(item['price'])

        return OrderResponse(**order)
    finally:
        cur.close()
        conn.close()


# ✅ Get orders by customer
@router.get("/customer/{customer_id}", response_model=List[OrderSummary])
def get_customer_orders(customer_id: int):
    customer_orders = orders.get_orders_by_customer(customer_id)
    if not customer_orders:
        return []

    response_orders = []
    for order in customer_orders:
        order_summary = {
            'id': order['id'],
            'customer_id': order['customer_id'],
            'restaurant_id': order['restaurant_id'],
            'total_price': float(order['total_price']),
            'status': order['status'],
            'payment_status': order['payment_status'],
            'created_at': order['created_at'],
            'restaurant_name': order['restaurant_name'],
            'items': [
                {
                    'id': item['id'],
                    'menu_item_id': item['menu_item_id'],
                    'name': item['name'],
                    'price': float(item['price']),
                    'quantity': item['quantity']
                }
                for item in order.get('items', [])
            ]
        }
        response_orders.append(OrderSummary(**order_summary))

    return response_orders


# ✅ Get orders by restaurant
@router.get("/restaurant/{restaurant_id}", response_model=List[OrderResponse])
def get_restaurant_orders(restaurant_id: int):
    restaurant_orders = orders.get_orders_by_restaurant(restaurant_id)
    response_orders = []
    for order in restaurant_orders:
        # Manually cast Decimal types to float for Pydantic validation
        order['total_price'] = float(order['total_price'])
        for item in order.get('items', []):
            item['price'] = float(item['price'])
        response_orders.append(OrderResponse(**order))
    return response_orders


# ✅ Update order status
@router.patch("/{order_id}", response_model=OrderResponse)
def update_order_status(order_id: int, order_update: OrderUpdate):
    updated_order = orders.update_order_status(order_id, order_update.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Manually cast Decimal types to float for Pydantic validation
    updated_order['total_price'] = float(updated_order['total_price'])
    for item in updated_order['items']:
        item['price'] = float(item['price'])

    return OrderResponse(**updated_order)


# ✅ Delete order
@router.delete("/{order_id}")
def delete_order(order_id: int):
    deleted = orders.delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully", "id": deleted['id']}