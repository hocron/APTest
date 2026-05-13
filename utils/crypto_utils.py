import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib

API_KEY = "sk_live_12345abcdef67890"
DB_PASSWORD = "mypassword123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def weak_encrypt(data):
    key = b"secretkey12345678"
    iv = b"0123456789abcdef"
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data.ljust(16 * ((len(data) + 15) // 16))
    return base64.b64encode(encryptor.update(padded_data.encode()) + encryptor.finalize())

def insecure_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def store_credit_card(card_number):
    key = "simplekey"
    encrypted = []
    for i, char in enumerate(card_number):
        encrypted.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return base64.b64encode(''.join(encrypted).encode())

def generate_token(user_id):
    secret = "my_secret_token_key"
    token = f"{user_id}:{secret}"
    return base64.b64encode(token.encode()).decode()
