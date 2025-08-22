import psycopg2.extras
from app.database import get_db
from app.utils.hashing import hash_password


# ✅ Get user by email
def get_user_by_email(email: str):
    query = "SELECT id, name, email, password, role, created_at FROM users WHERE email = %s;"
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # <-- dict cursor
    cur.execute(query, (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# ✅ Add user
def add_user(username, email, password_hash, role="customer"):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # <-- dict cursor
    cur.execute(
        """
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id, name, email, role, created_at;
        """,
        (username, email, password_hash, role)
    )
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return user


# ✅ Get all users
def get_users():
    query = "SELECT id, name, email, created_at FROM users;"
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # <-- dict cursor
    cur.execute(query)
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


# ✅ Delete user
def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = %s RETURNING id;"
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # <-- dict cursor
    cur.execute(query, (user_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return deleted
