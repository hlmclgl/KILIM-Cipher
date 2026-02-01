import time
import secrets
import hmac
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20

def generate_random_data(size):
    return secrets.token_bytes(size)

def aes_encrypt(key, data):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad_length = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_length] * pad_length)
    return iv + cipher.encrypt(padded_data)

def aes_decrypt(key, enc_data):
    iv, ciphertext = enc_data[:16], enc_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    pad_length = decrypted[-1]
    return decrypted[:-pad_length]

def chacha_encrypt(key, data):
    cipher = ChaCha20.new(key=key)
    return cipher.nonce + cipher.encrypt(data)

def chacha_decrypt(key, enc_data):
    nonce, ciphertext = enc_data[:8], enc_data[8:]
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ciphertext)

class SimpleEncryption:
    def __init__(self):
        self.hmac_key = secrets.token_bytes(32)
    
    def encrypt(self, message):
        seed = secrets.randbelow(256 - 1) + 1
        seed_bytes = seed.to_bytes(4, 'big')
        hmac_digest = hmac.new(self.hmac_key, seed_bytes, hashlib.sha256).digest()
        encrypted = base64.urlsafe_b64encode(hmac_digest + seed_bytes + message).decode()
        return encrypted

    def decrypt(self, cipher_text):
        decoded = base64.urlsafe_b64decode(cipher_text.encode())
        return decoded[36:]

data_sizes = [16, 64, 256, 1024]  
key_aes = get_random_bytes(32)
key_chacha = get_random_bytes(32)
custom_encryption = SimpleEncryption()

performance_results = []

for size in data_sizes:
    data = generate_random_data(size)

    start = time.time()
    enc_aes = aes_encrypt(key_aes, data)
    aes_enc_time = time.time() - start

    start = time.time()
    dec_aes = aes_decrypt(key_aes, enc_aes)
    aes_dec_time = time.time() - start

    start = time.time()
    enc_chacha = chacha_encrypt(key_chacha, data)
    chacha_enc_time = time.time() - start

    start = time.time()
    dec_chacha = chacha_decrypt(key_chacha, enc_chacha)
    chacha_dec_time = time.time() - start

    start = time.time()
    enc_custom = custom_encryption.encrypt(data)
    custom_enc_time = time.time() - start

    start = time.time()
    dec_custom = custom_encryption.decrypt(enc_custom)
    custom_dec_time = time.time() - start

    performance_results.append({
        "Data Size": size,
        "AES Encrypt Time (s)": aes_enc_time,
        "AES Decrypt Time (s)": aes_dec_time,
        "ChaCha20 Encrypt Time (s)": chacha_enc_time,
        "ChaCha20 Decrypt Time (s)": chacha_dec_time,
        "Custom Encrypt Time (s)": custom_enc_time,
        "Custom Decrypt Time (s)": custom_dec_time,
    })

performance_results
