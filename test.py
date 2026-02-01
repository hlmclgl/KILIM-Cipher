from encryption_manager import EncryptionManager
import secrets

key = secrets.token_bytes(32)
enc = EncryptionManager(key)

def generate_nist_singleline(bit_target=1_000_000, output_file="nist_input.txt"):

    bitstream = []

    while len("".join(bitstream)) < bit_target:

        msg = secrets.token_hex(32)
        cipher = enc.encrypt(msg)

        if isinstance(cipher, bytes):
            cipher = cipher.hex()

        cipher_str = str(cipher)
        cipher_bytes = cipher_str.encode("utf-8")

        bits = ''.join(f"{byte:08b}" for byte in cipher_bytes)

        bitstream.append(bits)

    final_bits = ''.join(bitstream)[:bit_target]

    try:
        with open(output_file, "w", newline="\n") as f:
            f.write(final_bits)
        print(f"{output_file} oluşturuldu. Uzunluk: {len(final_bits)} bit")
    except Exception as e:
        print("Dosya yazma hatası:", e)

generate_nist_singleline()
