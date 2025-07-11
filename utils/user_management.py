from database import create_connection
import re
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
    
def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()
    col_names = [col[0] for col in cursor.description]
    cursor.close()
    return [dict(zip(col_names, row)) for row in rows]

def create_user(nama_lengkap, username, password, role="user"):
    conn = create_connection()
    cursor = conn.cursor()

    # Validasi email (username)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
        return "email_invalid"

    # Cek apakah username sudah ada
    cursor.execute("SELECT COUNT(*) FROM user WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        return "username_exists"

    # Simpan ke database
    hashed = hash_password(password)
    cursor.execute("""
        INSERT INTO user (nama_lengkap, username, password, role)
        VALUES (%s, %s, %s, %s)
    """, (nama_lengkap, username, hashed, role))
    conn.commit()
    cursor.close()
    return "success"

def update_user_role(user_id, new_role):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET role = %s WHERE id_user = %s", (new_role, user_id))
    conn.commit()
    cursor.close()
    return True

def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id_user = %s", (user_id,))
    conn.commit()
    cursor.close()
    return True
