import time
import os
import sys
import hashlib
import hmac
import secrets
import random
import statistics

# Bellek ölçümü (Varsa kullanılır, yoksa hata vermez)
try:
    import tracemalloc
    TRACEMALLOC_AVAILABLE = True
except ImportError:
    TRACEMALLOC_AVAILABLE = False

# ==========================================
# KILIM ALGORİTMASI SİMÜLASYONU
# ==========================================
class KILIM_Simulated:
    def __init__(self, master_key):
        self.master_key = master_key
        self.N = 269 
        # Tabloyu bellekte tutma simülasyonu
        self.table_enc = list(range(self.N))
        self.table_dec = list(range(self.N))

    def encrypt_text(self, text_data):
        # 1. HMAC & Tablo Kurulumu
        iv = secrets.token_bytes(4)
        seed = hmac.new(self.master_key, iv, hashlib.sha256).digest()
        
        # Tablo karıştırma (Fisher-Yates)
        random.seed(seed)
        random.shuffle(self.table_enc)
        
        # 2. Şifreleme Döngüsü
        prev_index = int.from_bytes(iv, 'big') % self.N
        encrypted_indices = []
        
        for byte_val in text_data:
            idx = byte_val % self.N
            current_dynamic_index = (idx + prev_index) % self.N
            cipher_val = self.table_enc[current_dynamic_index]
            encrypted_indices.append(cipher_val)
            prev_index = current_dynamic_index
            
        return encrypted_indices

    def decrypt_text(self, encrypted_indices):
        # 1. Kurulum
        iv = secrets.token_bytes(4)
        seed = hmac.new(self.master_key, iv, hashlib.sha256).digest()
        random.seed(seed)
        random.shuffle(self.table_dec)
        
        # 2. Çözme Döngüsü
        prev_index = int.from_bytes(iv, 'big') % self.N
        decrypted_indices = []
        
        for cipher_val in encrypted_indices:
            # Ters işlem simülasyonu
            try:
                current_dynamic_index = self.table_dec.index(cipher_val)
            except ValueError:
                current_dynamic_index = 0
            
            original_idx = (current_dynamic_index - prev_index) % self.N
            decrypted_indices.append(original_idx)
            prev_index = current_dynamic_index
            
        return decrypted_indices

# ==========================================
# TEST MOTORU
# ==========================================
def run_table1_benchmark():
    # Değişkenleri baştan tanımlayalım (Hata önleyici)
    avg_enc_ms = 0.0
    avg_dec_ms = 0.0
    mb_time_sec = 0.0
    peak_memory_kb = 0.0
    table_size_kb = 0.0

    print(f"{'='*60}")
    print(f"BENCHMARK BAŞLATILIYOR... (Lütfen bekleyin)")
    print(f"{'='*60}", flush=True)
    
    key = os.urandom(32)
    cipher = KILIM_Simulated(key)
    
    # ---------------------------------------------------------
    # TEST 1: 1 KB İşlem Hızı (Ortalama)
    # ---------------------------------------------------------
    print("-> Test 1: 1 KB veri için hız testi yapılıyor...", end=" ", flush=True)
    kb_data = b'a' * 1024 # 1 KB
    iterations = 1000     
    
    enc_times = []
    dec_times = []
    
    # Isınma turu
    cipher.encrypt_text(kb_data)

    for _ in range(iterations):
        # Encrypt
        t1 = time.perf_counter()
        enc_res = cipher.encrypt_text(kb_data)
        t2 = time.perf_counter()
        enc_times.append((t2 - t1) * 1000) # ms'ye çevir
        
        # Decrypt
        t3 = time.perf_counter()
        cipher.decrypt_text(enc_res)
        t4 = time.perf_counter()
        dec_times.append((t4 - t3) * 1000) # ms'ye çevir

    avg_enc_ms = statistics.mean(enc_times)
    avg_dec_ms = statistics.mean(dec_times)
    print("TAMAMLANDI.")
    
    # ---------------------------------------------------------
    # TEST 2: 1 MB Şifreleme Süresi
    # ---------------------------------------------------------
    print("-> Test 2: 1 MB büyük veri testi yapılıyor...", end=" ", flush=True)
    mb_data = b'a' * 1024 * 1024 # 1 MB
    t_start = time.perf_counter()
    cipher.encrypt_text(mb_data)
    t_end = time.perf_counter()
    mb_time_sec = t_end - t_start
    print("TAMAMLANDI.")

    # ---------------------------------------------------------
    # TEST 3: Bellek Kullanımı
    # ---------------------------------------------------------
    print("-> Test 3: Bellek analizi yapılıyor...", end=" ", flush=True)
    
    # Tablo boyutu hesaplama
    table_size_bytes = sys.getsizeof(cipher.table_enc) + sum(sys.getsizeof(i) for i in cipher.table_enc)
    table_size_kb = table_size_bytes / 1024

    if TRACEMALLOC_AVAILABLE:
        tracemalloc.start()
        _ = cipher.encrypt_text(kb_data)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_kb = peak / 1024
    print("TAMAMLANDI.")

    # ---------------------------------------------------------
    # SONUÇ TABLOSU
    # ---------------------------------------------------------
    print(f"\n{'-'*60}")
    print(f"TABLO 1 İÇİN SONUÇLAR (Kopyalayabilirsiniz)")
    print(f"{'-'*60}")
    print(f"| Metric                          | Value          |")
    print(f"|---------------------------------|----------------|")
    print(f"| Average Encryption Time (1 KB)  | {avg_enc_ms:.4f} ms      |")
    print(f"| Average Decryption Time (1 KB)  | {avg_dec_ms:.4f} ms      |")
    print(f"| 1 MB Encryption Time            | {mb_time_sec:.4f} seconds  |")
    
    if TRACEMALLOC_AVAILABLE:
        print(f"| Memory Usage (1 KB Processing)  | ~{peak_memory_kb:.2f} KB       |")
    else:
        print(f"| Memory Usage (1 KB Processing)  | N/A            |")
        
    print(f"| Table Memory (269 Characters)   | ~{table_size_kb:.2f} KB       |")
    print(f"{'-'*60}")

if __name__ == "__main__":
    run_table1_benchmark()