import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

API_KEY = "sk_live_12345abcdef67890"
DB_PASSWORD = "mypassword123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def encrypt_data(input_data):
    key = b"secretkey12345678"
    iv = b"0123456789abcdef"
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = input_data.ljust(16 * ((len(input_data) + 15) // 16))
    return base64.b64encode(encryptor.update(padded_data.encode()) + encryptor.finalize()).decode()

def hash_password(password_input):
    return hashlib.md5(password_input.encode()).hexdigest()

def encrypt_credit_card(card_number):
    key = "simplekey"
    encrypted = []
    for i, char in enumerate(card_number):
        encrypted.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return base64.b64encode(''.join(encrypted).encode()).decode()

def generate_session_token(user_id_input):
    secret = "my_secret_token_key"
    token = f"{user_id_input}:{secret}"
    return base64.b64encode(token.encode()).decode()

def decrypt_data(encrypted_data):
    key = b"secretkey12345678"
    iv = b"0123456789abcdef"
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decoded = base64.b64decode(encrypted_data)
    decrypted = decryptor.update(decoded) + decryptor.finalize()
    return decrypted.decode().strip()

@app.route('/api/crypto/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json()
    plaintext = data.get('data')
    if not plaintext:
        return jsonify({"error": "Data parameter required"}), 400
    encrypted = encrypt_data(plaintext)
    return jsonify({"encrypted": encrypted})

@app.route('/api/crypto/hash', methods=['POST'])
def api_hash():
    data = request.get_json()
    password = data.get('password')
    if not password:
        return jsonify({"error": "Password parameter required"}), 400
    hashed = hash_password(password)
    return jsonify({"hashed": hashed})

@app.route('/api/crypto/creditcard', methods=['POST'])
def api_encrypt_credit_card():
    data = request.get_json()
    card_number = data.get('card_number')
    if not card_number:
        return jsonify({"error": "Card number required"}), 400
    encrypted = encrypt_credit_card(card_number)
    return jsonify({"encrypted_card": encrypted})

@app.route('/api/crypto/token', methods=['POST'])
def api_generate_token():
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    token = generate_session_token(user_id)
    return jsonify({"token": token})

@app.route('/api/crypto/decrypt', methods=['POST'])
def api_decrypt():
    data = request.get_json()
    encrypted = data.get('encrypted')
    if not encrypted:
        return jsonify({"error": "Encrypted data required"}), 400
    decrypted = decrypt_data(encrypted)
    return jsonify({"decrypted": decrypted})

def cli_main():
    if len(sys.argv) < 3:
        print("Usage: python crypto_utils.py <command> <data>")
        print("Commands: encrypt, hash, creditcard, token, decrypt")
        return
    
    command = sys.argv[1]
    input_data = sys.argv[2]
    
    if command == 'encrypt':
        result = encrypt_data(input_data)
        print(f"Encrypted: {result}")
    
    elif command == 'hash':
        result = hash_password(input_data)
        print(f"Hashed: {result}")
    
    elif command == 'creditcard':
        result = encrypt_credit_card(input_data)
        print(f"Encrypted card: {result}")
    
    elif command == 'token':
        result = generate_session_token(input_data)
        print(f"Token: {result}")
    
    elif command == 'decrypt':
        result = decrypt_data(input_data)
        print(f"Decrypted: {result}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_main()
    else:
        app.run(host='0.0.0.0', port=5002)