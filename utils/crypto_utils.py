import hashlib, base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flask import Flask, request

app = Flask(__name__)

API_KEY = "sk_live_12345abcdef"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLE"

def weak_encrypt(data):
    key = b"secretkey12345678"
    iv = b"0123456789abcdef"
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    return base64.b64encode(cipher.encryptor().update(data.ljust(16).encode())).decode()

def hash_pass(password):
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json()
    return {'encrypted': weak_encrypt(data['data'])}

@app.route('/api/hash', methods=['POST'])
def api_hash():
    data = request.get_json()
    return {'hash': hash_pass(data['password'])}

if __name__ == '__main__':
    app.run(port=5002)
