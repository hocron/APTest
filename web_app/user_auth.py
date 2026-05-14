import sqlite3
from flask import Flask, request

app = Flask(__name__)

SECRET_KEY = "supersecretkey12345"

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '" + username + "'")
    return cursor.fetchone()

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
    return cursor.fetchone() is not None

@app.route('/api/user')
def api_user():
    return str(get_user(request.args.get('username')))

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    return {'ok': authenticate(data['username'], data['password'])}

if __name__ == '__main__':
    app.run(port=5000)
