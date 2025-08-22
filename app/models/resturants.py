# # app/models/restaurants.py
# from app.database import get_db

# # ✅ Create table (run once during setup/migrations)
# def create_restaurants_table():
#     query = """
#     CREATE TABLE IF NOT EXISTS restaurants (
#         id SERIAL PRIMARY KEY,
#         name VARCHAR(200) NOT NULL,
#         description TEXT,
#         address VARCHAR(300),
#         phone VARCHAR(20),
#         created_at TIMESTAMP DEFAULT NOW()
#     );
#     """
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(query)
#     conn.commit()
#     cur.close()
#     conn.close()


# # ✅ Add new restaurant
# def add_restaurant(name, description=None, address=None, phone=None):
#     query = """
#     INSERT INTO restaurants (name, description, address, phone)
#     VALUES (%s, %s, %s, %s)
#     RETURNING id, name, description, address, phone, created_at;
#     """
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(query, (name, description, address, phone))
#     result = cur.fetchone()
#     conn.commit()
#     cur.close()
#     conn.close()
#     return result


# # ✅ Get all restaurants
# def get_restaurants():
#     query = "SELECT id,created_at FROM restaurants;"
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(query)
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return rows


# # ✅ Get single restaurant
# def get_restaurant_by_id(rest_id):
#     query = "SELECT id, name, description, address, phone, created_at FROM restaurants WHERE id = %s;"
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(query, (rest_id,))
#     row = cur.fetchone()
#     cur.close()
#     conn.close()
#     return row


# # ✅ Delete restaurant
# def delete_restaurant(rest_id):
#     query = "DELETE FROM restaurants WHERE id = %s RETURNING id;"
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(query, (rest_id,))
#     result = cur.fetchone()
#     conn.commit()
#     cur.close()
#     conn.close()
#     return result
# app/models/restaurants.py
from app.database import get_db
from app.schemas.restaurant import  RestaurantResponse

def create_restaurants_table():
    query = """
    CREATE TABLE IF NOT EXISTS restaurants (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        description TEXT,
        address VARCHAR(300),
        phone VARCHAR(20),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def add_restaurant(name, description=None, address=None, phone=None):
    query = """
    INSERT INTO restaurants (name, description, address, phone)
    VALUES (%s, %s, %s, %s)
    RETURNING id, name, description, address, phone, created_at;
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (name, description, address, phone))
    row = cur.fetchone()   # 👈 now dict
    conn.commit()
    cur.close()
    conn.close()
    return row


def get_restaurants():
    query = "SELECT id, name FROM restaurants;"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()  # 👈 list[dict]
    cur.close()
    conn.close()
    return rows


# def get_restaurant_by_id(rest_id):
#     query = "SELECT id, name, description, address, phone, created_at FROM restaurants WHERE id = %s;"
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(query, (rest_id,))
#     row = cur.fetchone()
#     cur.close()
#     conn.close()
#     return row


def get_restaurant_by_id(rest_id: int):
    query = """
        SELECT id, name, description, address, phone, created_at
        FROM restaurants
        WHERE id = %s;
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (rest_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return RestaurantResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            address=row["address"],
            phone=row["phone"],
            created_at=row["created_at"]
        )
    return None


def delete_restaurant(rest_id):
    query = "DELETE FROM restaurants WHERE id = %s RETURNING id;"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (rest_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row
