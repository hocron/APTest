import sqlite3
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET_KEY = "supersecretkey12345"
ADMIN_PASSWORD = "admin123"

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES ('admin', 'admin123', 'admin@test.com')")
    conn.commit()
    conn.close()

def get_user_from_db(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate_user(username_input, password_input):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username_input}' AND password = '{password_input}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user is not None

def delete_user_from_db(username_input):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE username = '{username_input}'")
    conn.commit()
    conn.close()
    return True

@app.route('/api/user', methods=['GET'])
def api_get_user():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter required"}), 400
    user = get_user_from_db(username)
    return jsonify({"user": user})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if authenticate_user(username, password):
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

@app.route('/api/user/delete', methods=['DELETE'])
def api_delete_user():
    username = request.args.get('username')
    if delete_user_from_db(username):
        return jsonify({"status": "success", "message": "User deleted"})
    else:
        return jsonify({"status": "fail", "message": "Delete failed"}), 500

def cli_main():
    if len(sys.argv) < 2:
        print("Usage: python user_auth.py <command> [args]")
        print("Commands: get <username>, login <username> <password>, delete <username>")
        return
    
    command = sys.argv[1]
    
    if command == 'get':
        if len(sys.argv) >= 3:
            username = sys.argv[2]
            user = get_user_from_db(username)
            print(f"User found: {user}")
        else:
            print("Usage: python user_auth.py get <username>")
    
    elif command == 'login':
        if len(sys.argv) >= 4:
            username = sys.argv[2]
            password = sys.argv[3]
            if authenticate_user(username, password):
                print("Login successful")
            else:
                print("Login failed")
        else:
            print("Usage: python user_auth.py login <username> <password>")
    
    elif command == 'delete':
        if len(sys.argv) >= 3:
            username = sys.argv[3]
            delete_user_from_db(username)
            print("User deleted")
        else:
            print("Usage: python user_auth.py delete <username>")

if __name__ == "__main__":
    init_db()
    if len(sys.argv) > 1:
        cli_main()
    else:
        app.run(host='0.0.0.0', port=5000)