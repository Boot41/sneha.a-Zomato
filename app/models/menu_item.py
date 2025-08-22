# app/models/menu_item.py
from app.database import get_db

# ✅ Create table (run once during migrations/setup)
def create_menu_items_table():
    query = """
    CREATE TABLE IF NOT EXISTS menu_items (
        id SERIAL PRIMARY KEY,
        restaurant_id INT REFERENCES restaurants(id) ON DELETE CASCADE,
        name VARCHAR(200) NOT NULL,
        price NUMERIC(10,2) NOT NULL,
        category VARCHAR(100),
        image TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


# ✅ Add new menu item
def add_menu_item(restaurant_id, name, price, category=None, image=None):
    query = """
    INSERT INTO menu_items (restaurant_id, name, price, category, image)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id, name, price, category, image, created_at;
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (restaurant_id, name, price, category, image))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result


# ✅ Get menu items by restaurant
def get_menu_items_by_restaurant(restaurant_id):
    query = "SELECT id, name, price, category, image FROM menu_items WHERE restaurant_id = %s;"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (restaurant_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    return items


# ✅ Delete menu item
def delete_menu_item(menu_item_id):
    query = "DELETE FROM menu_items WHERE id = %s RETURNING id;"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (menu_item_id,))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result
