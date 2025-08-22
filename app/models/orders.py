# app/models/orders.py
from app.database import get_db

# ✅ Create table (run once during migrations/setup)
def create_order_items_table():
    query = """
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INT REFERENCES orders(id) ON DELETE CASCADE,
        menu_item_id INT REFERENCES menu_items(id) ON DELETE CASCADE,
        quantity INT NOT NULL,
        price NUMERIC(10, 2) NOT NULL
    );
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def create_orders_table():
    query = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES users(id) ON DELETE CASCADE,
        restaurant_id INT REFERENCES restaurants(id) ON DELETE CASCADE,
        total_price NUMERIC(10,2) NOT NULL,
        status VARCHAR(20) CHECK (status IN ('placed', 'delivered')) DEFAULT 'placed',
        payment_status VARCHAR(10) DEFAULT 'Unpaid',
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


# ✅ Create new order
def create_order(customer_id, restaurant_id, total_price, items, payment_status='Unpaid'):
    conn = get_db()
    cur = conn.cursor()
    try:
        # Insert the main order record
        query = """
        INSERT INTO orders (customer_id, restaurant_id, total_price, payment_status)
        VALUES (%s, %s, %s, %s) RETURNING id;
        """
        cur.execute(query, (customer_id, restaurant_id, total_price, payment_status))
        order_id = cur.fetchone()['id']

        # Insert order items
        items_query = """
        INSERT INTO order_items (order_id, menu_item_id, quantity, price)
        VALUES (%s, %s, %s, %s);
        """
        for item in items:
            cur.execute(items_query, (order_id, item['menu_item_id'], item['quantity'], item['price']))

        # Fetch the complete order details to return
        full_order = get_order_by_id(cur, order_id)
        conn.commit()
        return full_order
    except Exception as e:
        conn.rollback()
        # It's good practice to log the error here
        print(f"Error creating order: {e}")
        return None
    finally:
        cur.close()
        conn.close()


# ✅ Get order by ID
def get_order_by_id(cur, order_id):
    query = """
    SELECT o.id, o.customer_id, o.restaurant_id, o.total_price, o.status, o.created_at, o.payment_status, r.name as restaurant_name
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.id
    WHERE o.id = %s;
    """
    cur.execute(query, (order_id,))
    order_data = cur.fetchone()

    if not order_data:
        return None

    order = dict(order_data)
    order['items'] = get_order_items_by_order_id(cur, order['id'])
    return order


# ✅ Get orders by customer
def get_orders_by_customer(customer_id):
    conn = get_db()
    cur = conn.cursor()
    try:
        # First get all orders for the customer
        query = """
        SELECT o.*, r.name as restaurant_name
        FROM orders o
        JOIN restaurants r ON o.restaurant_id = r.id
        WHERE o.customer_id = %s
        ORDER BY o.created_at DESC;
        """
        cur.execute(query, (customer_id,))
        orders = cur.fetchall()

        # For each order, get its items with menu item names
        result = []
        for order in orders:
            order_dict = dict(order)
            items_query = """
            SELECT oi.*, mi.name
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = %s;
            """
            cur.execute(items_query, (order['id'],))
            items = cur.fetchall()
            
            # Convert Decimal to float for JSON serialization
            order_dict['total_price'] = float(order_dict['total_price'])
            order_dict['items'] = [{
                'id': item['id'],
                'menu_item_id': item['menu_item_id'],
                'name': item['name'],
                'quantity': item['quantity'],
                'price': float(item['price'])
            } for item in items]
            
            result.append(order_dict)

        return result
    except Exception as e:
        print(f"Error getting orders by customer: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_order_items_by_order_id(cur, order_id):
    query = """
    SELECT oi.id, mi.name, oi.price, oi.quantity, oi.menu_item_id
    FROM order_items oi
    JOIN menu_items mi ON oi.menu_item_id = mi.id
    WHERE oi.order_id = %s
    """
    cur.execute(query, (order_id,))
    items = cur.fetchall()
    return [dict(item) for item in items]

# Get orders by restaurant
def get_orders_by_restaurant(restaurant_id):
    conn = get_db()
    cur = conn.cursor()
    try:
        query = """SELECT o.id, o.customer_id, o.restaurant_id, o.total_price, o.status, o.created_at, o.payment_status, r.name as restaurant_name
        FROM orders o
        JOIN restaurants r ON o.restaurant_id = r.id
        WHERE o.restaurant_id = %s ORDER BY o.created_at DESC;"""
        cur.execute(query, (restaurant_id,))
        orders_data = cur.fetchall()

        orders = []
        for order_data in orders_data:
            order = dict(order_data)
            order['items'] = get_order_items_by_order_id(cur, order['id'])
            orders.append(order)
        return orders
    finally:
        cur.close()
        conn.close()


# ✅ Update order status
def update_order_status(order_id, status):
    conn = get_db()
    cur = conn.cursor()
    try:
        query = """
        UPDATE orders 
        SET status = %s 
        WHERE id = %s 
        RETURNING id;
        """
        cur.execute(query, (status, order_id))
        result = cur.fetchone()
        if not result:
            return None
        
        # After updating, fetch the full order details
        updated_order = get_order_by_id(cur, order_id)
        conn.commit()
        return updated_order
    except Exception as e:
        conn.rollback()
        print(f"Error updating order status: {e}")
        return None
    finally:
        cur.close()
        conn.close()


# ✅ Delete order
def delete_order(order_id):
    query = "DELETE FROM orders WHERE id = %s RETURNING id;"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (order_id,))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if result:
        return dict(result)
    return None