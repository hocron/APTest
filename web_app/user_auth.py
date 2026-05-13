import sqlite3
import sys

SECRET_KEY = "supersecretkey12345"
ADMIN_PASSWORD = "admin123"

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user is not None

def delete_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE username = '{username}'")
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        user = get_user(username)
        print(f"User found: {user}")
