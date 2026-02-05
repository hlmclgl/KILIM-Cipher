import os
import secrets
import math
import random
import string
import time
import multiprocessing
import sys
import traceback
from encryption_manager import EncryptionManager 

OUTPUT_FILENAME = "nist_large_750MB.bin"
TARGET_SIZE_MB = 750  
MASTER_KEY = secrets.token_bytes(32)

def worker_generate_chunk(args):
    try:
        target_chunk_size, char_map, key, seed, task_id = args
        
        random.seed(seed + task_id)
        
        manager = EncryptionManager(key)
        
        
        internal_batch_size = 10000 
        base_chars = string.ascii_letters + string.digits + string.punctuation
        
        byte_chunk = bytearray()
        bit_buffer = 0
        bits_in_buffer = 0
        
        while len(byte_chunk) < target_chunk_size:
            dummy_text = "".join(random.choices(base_chars, k=internal_batch_size))
            
            cipher_text = manager.encrypt(dummy_text)
            
            for char in cipher_text:
                if char not in char_map:
                    continue
                
                val = char_map[char]
                
                if val < 128:
                    bit_buffer = (bit_buffer << 7) | val
                    bits_in_buffer += 7
                    
                    while bits_in_buffer >= 8:
                        bits_in_buffer -= 8
                        byte_val = (bit_buffer >> bits_in_buffer) & 0xFF
                        byte_chunk.append(byte_val)
                        
                        if len(byte_chunk) >= target_chunk_size:
                            return byte_chunk
        
        return byte_chunk

    except Exception as e:
        return f"ERROR: {str(e)} | {traceback.format_exc()}"

def generate_safe_random_text(length):
    base_chars = string.ascii_letters + string.digits + string.punctuation + " "
    turkish_chars = "çğıöşüÇĞİÖŞÜ"
    return "".join(random.choices(base_chars + turkish_chars, k=length))

def main():
    multiprocessing.freeze_support()

    print("=" * 60)
    print(f"🚀 NİHAİ TEST VERİSİ ÜRETİCİSİ V2 (Hedef: {TARGET_SIZE_MB} MB)")
    print(f"İşlemci Çekirdek Sayısı: {multiprocessing.cpu_count()}")
    print("=" * 60)
    
    print("1. AŞAMA: Sistem Kontrolü ve Havuz Analizi...")
    
    manager = EncryptionManager(MASTER_KEY)
    learning_input = generate_safe_random_text(10000)
    try:
        cipher_sample = manager.encrypt(learning_input)
    except Exception as e:
        print(f"❌ BAŞLANGIÇ HATASI: EncryptionManager çalışmıyor!\nHata: {e}")
        return

    unique_chars = sorted(list(set(cipher_sample)))
    char_map = {char: idx for idx, char in enumerate(unique_chars)}
    
    if len(unique_chars) < 128:
        print(f"❌ KRİTİK HATA: Algoritma sadece {len(unique_chars)} karakter üretiyor. 128+ gerekli.")
        return
    print(f"✅ Analiz Tamam: {len(unique_chars)} karakter tespit edildi.")

    print("-" * 60)
    print("2. AŞAMA: Üretim Başlıyor (Hızlı Güncelleme Modu)...")
    
    start_time = time.time()
    

    total_bytes_needed = TARGET_SIZE_MB * 1024 * 1024
    chunk_size = 50 * 1024  
    num_tasks = math.ceil(total_bytes_needed / chunk_size)
    
    print(f"Toplam Görev Sayısı: {num_tasks} (Her biri {chunk_size/1024:.0f} KB)")
    
    tasks = [(chunk_size, char_map, MASTER_KEY, i, i) for i in range(num_tasks)]
    
    total_written = 0
    
    with open(OUTPUT_FILENAME, "wb") as f:
        with multiprocessing.Pool() as pool:
            try:
                for i, result in enumerate(pool.imap_unordered(worker_generate_chunk, tasks)):
                    
                    if isinstance(result, str) and result.startswith("ERROR"):
                        print(f"\n\n❌ İŞÇİ HATASI: {result}")
                        pool.terminate()
                        return

                    f.write(result)
                    total_written += len(result)
                    
                    if i % 20 == 0 or total_written >= total_bytes_needed:
                        elapsed = time.time() - start_time
                        percent = (total_written / total_bytes_needed) * 100
                        
                        if elapsed < 0.1: elapsed = 0.1
                        speed = total_written / elapsed / (1024 * 1024) # MB/s
                        
                        remaining_bytes = total_bytes_needed - total_written
                        remaining_time = remaining_bytes / (speed * 1024 * 1024 + 0.001) / 60 # Minute
                        
                        bar_len = 30
                        filled_len = int(bar_len * percent / 100)
                        bar = '#' * filled_len + '-' * (bar_len - filled_len)
                        
                        sys.stdout.write(f"\r[{bar}] %5.1f%% | Hız: %5.2f MB/s | Kalan: ~%3.0f dk | Toplam: %4.0f MB" % 
                                         (percent, speed, remaining_time, total_written/(1024*1024)))
                        sys.stdout.flush()
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ İşlem kullanıcı tarafından durduruldu! Mevcut dosya korundu.")
                pool.terminate()
                pool.join()
                return

    print("\n" + "=" * 60)
    final_size = os.path.getsize(OUTPUT_FILENAME) / (1024*1024)
    print(f"✅ İŞLEM TAMAMLANDI!")
    print(f"Dosya: {OUTPUT_FILENAME}")
    print(f"Boyut: {final_size:.2f} MB")
    print(f"Toplam Süre: {(time.time() - start_time)/60:.1f} dakika")
    
    print("-" * 60)
    print("TEST KOMUTU (Linux/WSL):")
    print(f"dieharder -a -g 201 -f {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()