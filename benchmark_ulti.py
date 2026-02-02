import time
import os
import hashlib
import hmac
import secrets
import random

# Kütüphane kontrolü
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
    LIB_AVAILABLE = True
except ImportError:
    LIB_AVAILABLE = False
    print("UYARI: 'cryptography' kütüphanesi yüklü değil. AES ve ChaCha20 testi atlanacak.")

# ==========================================
# 1. RC4 IMPLEMENTATION (Pure Python)
# ==========================================
class RC4:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + self.key[i % len(self.key)]) % 256
            S[i], S[j] = S[j], S[i]

        i = j = 0
        res = []
        for b in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            res.append(b ^ S[(S[i] + S[j]) % 256])
        return bytes(res)

# ==========================================
# 2. STANDARD ALGORITHMS (AES & CHACHA20)
# ==========================================
def aes_encrypt(key, data):
    if not LIB_AVAILABLE: return None
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return iv + encryptor.update(padded_data) + encryptor.finalize()

def chacha20_encrypt(key, data):
    if not LIB_AVAILABLE: return None
    nonce = os.urandom(16)
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data)

# ==========================================
# 3. KILIM ALGORITHM (Proposed)
# ==========================================
class KILIM_Simulated:
    def __init__(self, master_key):
        self.master_key = master_key
        self.N = 269 # 256 ASCII + 13 TR
        
    def encrypt(self, text_data):
        # 1. HMAC Seed
        iv = secrets.token_bytes(4)
        seed = hmac.new(self.master_key, iv, hashlib.sha256).digest()
        
        # 2. Table Permutation Simulation
        table = list(range(self.N))
        random.seed(seed)
        random.shuffle(table)
        
        # 3. Dynamic Index Chaining
        prev_index = int.from_bytes(iv, 'big') % self.N
        
        # Fast processing simulation for benchmarking math operations
        # KILIM is fundamentally: (input + prev) % N -> Table Lookup
        data_indices = [b % 255 for b in text_data] # Simulate text index conversion
        
        encrypted_indices = []
        for idx in data_indices:
            current_dynamic_index = (idx + prev_index) % self.N
            cipher_val = table[current_dynamic_index]
            encrypted_indices.append(cipher_val)
            prev_index = current_dynamic_index
            
        return encrypted_indices

# ==========================================
# BENCHMARK ENGINE
# ==========================================
def run_benchmark():
    print(f"{'='*60}")
    print(f"ULTIMATE BENCHMARK: 1 MB DATA (Avg of 10 runs)")
    print(f"{'='*60}")

    dummy_data = os.urandom(1024 * 1024) # 1 MB
    key_32 = os.urandom(32)
    
    results = {}

    # --- TEST 1: RC4 (Baseline Stream Cipher) ---
    rc4 = RC4(key_32)
    times = []
    for _ in range(5): # RC4 is slow, 5 runs enough
        start = time.time()
        rc4.encrypt(dummy_data)
        times.append(time.time() - start)
    results['RC4 (Python)'] = sum(times) / len(times)
    print(f"RC4 (Python)      : {results['RC4 (Python)']:.5f} s")

    # --- TEST 2: KILIM (Proposed) ---
    kilim = KILIM_Simulated(key_32)
    times = []
    for _ in range(10):
        start = time.time()
        kilim.encrypt(dummy_data)
        times.append(time.time() - start)
    results['KILIM (Proposed)'] = sum(times) / len(times)
    print(f"KILIM (Proposed)  : {results['KILIM (Proposed)']:.5f} s")

    if LIB_AVAILABLE:
        # --- TEST 3: AES-256 (Block Standard) ---
        times = []
        for _ in range(10):
            start = time.time()
            aes_encrypt(key_32, dummy_data)
            times.append(time.time() - start)
        results['AES-256 (C-Lib)'] = sum(times) / len(times)
        print(f"AES-256 (Hardware): {results['AES-256 (C-Lib)']:.5f} s")

        # --- TEST 4: ChaCha20 (Modern Stream Standard) ---
        times = []
        for _ in range(10):
            start = time.time()
            chacha20_encrypt(key_32, dummy_data)
            times.append(time.time() - start)
        results['ChaCha20 (C-Lib)'] = sum(times) / len(times)
        print(f"ChaCha20 (Optimized): {results['ChaCha20 (C-Lib)']:.5f} s")

    print(f"\n{'-'*60}")
    print(f"FINAL RESULTS")
    print(f"{'-'*60}")
    print(f"| Algorithm        | Time (1MB) |")
    print(f"|------------------|------------|")
    for algo, t in results.items():
        print(f"| {algo:<16} | {t:.5f}s    |")
    print(f"{'-'*60}")

if __name__ == "__main__":
    run_benchmark()