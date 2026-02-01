
import secrets
import hmac
import hashlib
import base64
import random
from unicodedata import normalize

class EncryptionManager:
    def __init__(self, shared_key: bytes):
        if len(shared_key) < 32:
             raise ValueError("HMAC anahtarı en az 32 bayt olmalıdır.")
        self.hmac_key = shared_key
        
        turkish_characters = ["ç", "ğ", "ı", "İ", "ö", "ş", "ü", "Ç", "Ğ", "I", "Ö", "Ş", "Ü"]
        self.all_characters = list({
            normalize('NFKC', chr(i)) for i in range(256)
        }.union({
            normalize('NFKC', c) for c in turkish_characters
        }))
        self.n = len(self.all_characters) 
        self.char_to_index = {char: idx for idx, char in enumerate(self.all_characters)}
        
    def _generate_transformation_table(self, iv_bytes: bytes):
        
        hmac_digest = hmac.new(self.hmac_key, iv_bytes, hashlib.sha256).digest()
        
        deterministic_seed = int.from_bytes(hmac_digest[:8], 'big')
        
        rng = random.Random(deterministic_seed) 

        shuffled = self.all_characters[:]
        rng.shuffle(shuffled)

        transformation_table = {
            self.all_characters[i]: shuffled[i] for i in range(self.n)
        }
        reverse_table = {
            shuffled[i]: self.all_characters[i] for i in range(self.n)
        }
        return transformation_table, reverse_table

    def encrypt(self, message: str) -> str:
        
        iv_bytes = secrets.token_bytes(4)
        iv_int = int.from_bytes(iv_bytes, 'big')
        
        Te, _ = self._generate_transformation_table(iv_bytes)
        
        encrypted = []
        prev = iv_int % self.n 
        
        for char in message:
            try:
                idx = self.char_to_index[char]
                dynamic_idx = (idx + prev) % self.n
                encrypted_char = Te[self.all_characters[dynamic_idx]]
                encrypted.append(encrypted_char)
                prev = dynamic_idx
            except KeyError as e:
                raise ValueError(f"Geçersiz karakter: {e.args[0]}")
                
        
        msg_length = len(message)
        padding_length = secrets.randbelow(50) + 50
        random_chars = [secrets.choice(self.all_characters) for _ in range(padding_length)]
        encrypted += random_chars
        
        header_data = iv_bytes + msg_length.to_bytes(3, 'big')
        hmac_digest = hmac.new(self.hmac_key, header_data, hashlib.sha256).digest()
        full_header = hmac_digest + header_data
        encoded_header = base64.urlsafe_b64encode(full_header).decode().rstrip('=')
        
        return encoded_header + ''.join(encrypted)

    def decrypt(self, cipher_text: str) -> str:
        
        header_len_bytes = 32 + 4 + 3 
        encoded_header_length = (header_len_bytes * 4 + 2) // 3 
        encoded_header = cipher_text[:encoded_header_length].encode()
        cipher_body = cipher_text[encoded_header_length:]
        missing_padding = len(encoded_header) % 4
        if missing_padding:
            encoded_header += b'=' * (4 - missing_padding)
            
        full_header = base64.urlsafe_b64decode(encoded_header)
        
        hmac_received = full_header[:32]
        iv_bytes = full_header[32:36]
        msg_length = int.from_bytes(full_header[36:39], 'big')
        header_data = iv_bytes + msg_length.to_bytes(3, 'big')
        hmac_calculated = hmac.new(self.hmac_key, header_data, hashlib.sha256).digest()
        if not hmac.compare_digest(hmac_received, hmac_calculated):
            raise ValueError("HMAC bütünlük doğrulama başarısız. Mesaj değiştirilmiş.")

        _, Td = self._generate_transformation_table(iv_bytes)
        
        decrypted = []
        iv_int = int.from_bytes(iv_bytes, 'big')
        prev = iv_int % self.n 
        
        data_to_decrypt = cipher_body[:msg_length]
        
        for char in data_to_decrypt:
            try:
                transformed_char = Td[char]
                transformed_idx = self.char_to_index[transformed_char]
                
                original_idx = (transformed_idx - prev) % self.n
                
                decrypted.append(self.all_characters[original_idx])
                
                prev = transformed_idx
                
            except KeyError as e:
                raise ValueError(f"Geçersiz şifreli karakter, çözme başarısız: {e.args[0]}")
                
        return ''.join(decrypted)
    
