import hashlib
from database import create_connection

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(username):
    return hashlib.sha256(f"{username}_secure_token".encode()).hexdigest()

def save_user_token(username, token):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET token = %s WHERE username = %s", (token, username))
    conn.commit()
    conn.close()

def get_user_by_token(token):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE token = %s", (token,))
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate_user(username, password):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user['password'] == hash_password(password):
        return user
    return None
