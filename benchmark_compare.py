import time
import os
import hashlib
import hmac
import secrets
import random

# AES için gerekli kütüphane
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False
    print("UYARI: 'cryptography' kütüphanesi yüklü değil. AES testi atlanacak.")
    print("Yüklemek için: pip install cryptography")

# ==========================================
# 1. RC4 IMPLEMENTATION (Pure Python)
# ==========================================
class RC4:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        # Key Scheduling Algorithm (KSA)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + self.key[i % len(self.key)]) % 256
            S[i], S[j] = S[j], S[i]

        # Pseudo-Random Generation Algorithm (PRGA)
        i = j = 0
        res = []
        for b in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            res.append(b ^ S[(S[i] + S[j]) % 256])
        return bytes(res)

# ==========================================
# 2. AES-256 IMPLEMENTATION (Standard Lib)
# ==========================================
def aes_encrypt(key, data):
    if not AES_AVAILABLE: return None
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Padding (PKCS7) needed for block cipher
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    return iv + encryptor.update(padded_data) + encryptor.finalize()

# ==========================================
# 3. KILIM ALGORITHM (Simplified Logic)
# ==========================================
class KILIM_Simulated:
    """
    Makaledeki mantığın birebir Python simülasyonu.
    Performance ölçümü için kritik matematiksel işlemler dahildir.
    """
    def __init__(self, master_key):
        self.master_key = master_key
        # 256 ASCII + 13 Türkçe Karakter
        self.turkish_chars = "ÇĞİÖŞÜçğıöşüi" # Ekstra karakterler
        self.N = 256 + len(self.turkish_chars) 
        
    def encrypt(self, text_data):
        # 1. HMAC ile Seed Üretimi (Cost: O(1))
        iv = secrets.token_bytes(4)
        seed = hmac.new(self.master_key, iv, hashlib.sha256).digest()
        
        # 2. Tablo Permütasyonu (Cost: O(N)) - Fisher-Yates Simulation
        # Performans testi için random.shuffle kullanıyoruz (benzer maliyet)
        table = list(range(self.N))
        random.seed(seed)
        random.shuffle(table)
        
        # 3. Dynamic Index Chaining (Cost: O(n))
        encrypted_indices = []
        prev_index = int.from_bytes(iv, 'big') % self.N
        
        # Veriyi byte array gibi simüle ediyoruz (indexleme hızı için)
        # Gerçekte text -> index map yapılır, burada hız testi için direct range kullanacağız
        # 1MB text verisi integer array olarak:
        data_indices = [b % self.N for b in text_data] 
        
        for idx in data_indices:
            # Core Logic: I_k = (i_k + I_{k-1}) mod N
            current_dynamic_index = (idx + prev_index) % self.N
            
            # Substitution
            cipher_val = table[current_dynamic_index]
            encrypted_indices.append(cipher_val)
            
            # Update State
            prev_index = current_dynamic_index
            
        return encrypted_indices

# ==========================================
# BENCHMARK ENGINE
# ==========================================
def run_benchmark():
    print(f"{'='*60}")
    print(f"BENCHMARK STARTING: 1 MB DATA (Average of 10 runs)")
    print(f"{'='*60}")

    # 1. Generate 1 MB Random Data
    dummy_data_bytes = os.urandom(1024 * 1024) # 1 MB Bytes
    # KILIM is text based usually, but we simulate byte processing speed
    
    # Keys
    key_32 = os.urandom(32) # 256 bit key
    
    results = {}

    # --- TEST 1: RC4 ---
    rc4_cipher = RC4(key_32)
    times = []
    for _ in range(10):
        start = time.time()
        rc4_cipher.encrypt(dummy_data_bytes)
        times.append(time.time() - start)
    avg_rc4 = sum(times) / len(times)
    results['RC4'] = avg_rc4
    print(f"RC4 Average Time      : {avg_rc4:.5f} seconds")

    # --- TEST 2: AES-256 ---
    if AES_AVAILABLE:
        times = []
        for _ in range(10):
            start = time.time()
            aes_encrypt(key_32, dummy_data_bytes)
            times.append(time.time() - start)
        avg_aes = sum(times) / len(times)
        results['AES-256'] = avg_aes
        print(f"AES-256 Average Time  : {avg_aes:.5f} seconds")
    else:
        results['AES-256'] = "N/A"

    # --- TEST 3: KILIM (Proposed) ---
    kilim_cipher = KILIM_Simulated(key_32)
    times = []
    for _ in range(10):
        start = time.time()
        kilim_cipher.encrypt(dummy_data_bytes)
        times.append(time.time() - start)
    avg_kilim = sum(times) / len(times)
    results['KILIM (Proposed)'] = avg_kilim
    print(f"KILIM Average Time    : {avg_kilim:.5f} seconds")

    print(f"\n{'-'*60}")
    print(f"FINAL TABLE RESULTS (For Copying)")
    print(f"{'-'*60}")
    print(f"| Algorithm       | Time (1MB) |")
    print(f"|-----------------|------------|")
    print(f"| RC4             | {results['RC4']:.4f}s     |")
    if AES_AVAILABLE:
        print(f"| AES-256         | {results['AES-256']:.4f}s     |")
    print(f"| KILIM (Proposed)| {results['KILIM (Proposed)']:.4f}s     |")
    print(f"{'-'*60}")

if __name__ == "__main__":
    run_benchmark()