# KILIM-Cipher: Localized Probabilistic Stream Cipher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange.svg)]()

**KILIM** is a novel probabilistic stream cipher designed to provide robust security for localized character sets, specifically optimizing for **Turkish language support** in resource-constrained IoT environments.

This repository contains the reference implementation and the graphical user interface (GUI) for the research paper:
> **"Localized Cryptographic Security: A Probabilistic Stream Cipher Supporting Turkish Character Sets"**
> *Submitted to the Journal of Information Security and Applications (JISA)*.

---

## 🧶 What is KILIM?

The name **KILIM** is twofold:

1.  **Technical Acronym:** It stands for **K**eyed **I**ndex **L**inked **I**ntegrity **M**echanism.
2.  **Cultural Metaphor:** In Turkish culture, a *"Kilim"* is a traditional woven rug. Just as a Kilim is woven loop by loop, this algorithm weaves each character into the encryption stream using a **Dynamic Index Chaining** mechanism. The state of each character depends on the entire history of the weaving process, ensuring that no pattern is repeated.

---

## 🚀 Key Features

* **Native Turkish Support:** Operates on an expanded character pool ($N=269$), natively supporting characters like `ç, ğ, ı, ö, ş, ü` without encoding overhead.
* **Probabilistic Encryption:** Utilizing HMAC-SHA256 for dynamic table seeding, ensuring that the same plaintext results in different ciphertexts in every session.
* **Dynamic Index Chaining:** Features a state-dependent indexing mechanism ($I_k$) that links each character encryption to the entire preceding stream, mitigating frequency analysis.
* **User-Friendly Interface:** Includes a simple GUI (`main.py`) for testing encryption and decryption instantly.
* **Verified Randomness:** The algorithm passes **NIST STS** and **Dieharder** statistical randomness tests.

---

## 🛠️ Installation

Clone the repository to your local machine:

```bash
git clone [https://github.com/hlmclgl/KILIM-Cipher.git](https://github.com/hlmclgl/KILIM-Cipher.git)
cd KILIM-Cipher
```

Ensure you have **Python 3.10** or higher installed.
The project relies on standard Python libraries (`tkinter` for GUI, `hashlib`, `hmac`, `secrets`). No heavy external dependencies are required.

---

## 💻 Usage

You can use the cipher via the Graphical User Interface (GUI) or import it into your own Python scripts.

### Option 1: Using the GUI (Recommended)

To test the algorithm with a visual interface, simply run the `main.py` file:

```bash
python main.py
```

### How to use the interface:

1. **Enter Text:** Type your message (Turkish characters supported) into the input box.

2. **Encrypt:** Click the "Encrypt" button. The system generates a random key and displays the ciphertext.

3. **Decrypt:** Click the "Decrypt" button to retrieve the original text using the stored key.

### Option 2: Using as a Library
You can import the `EncryptionManager` class into your own projects:

```Python
import secrets
from encryption_manager import EncryptionManager

# 1. Generate a Master Key (32 bytes)
master_key = secrets.token_bytes(32)

# 2. Initialize the Cipher
cipher = EncryptionManager(master_key)

# 3. Encrypt (Native Turkish Support)
plaintext = "Merhaba Dünya! KİLİM Algoritması testi."
encrypted = cipher.encrypt(plaintext)
print(f"Ciphertext: {encrypted}")

# 4. Decrypt
decrypted = cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

# Integrity Check
assert plaintext == decrypted
```

## 🧪 Scientific Validation (NIST & Dieharder)
To validate the statistical randomness claims made in the paper, we provide scripts to generate large binary datasets suitable for the Dieharder and NIST STS test suites.

1. **Generate Test Data:** Run the generation script to create a large binary file (e.g., 750 MB) representing the cipher's output stream. This script uses multiprocessing and bit-packing to ensure uniform distribution:

```bash
python generate_nist_large.py
```

2. **Verify with Dieharder (Linux/WSL):** Once the data is generated, run the statistical tests:

```bash
dieharder -a -g 201 -f nist_large_750MB.bin
```

## ⚠️ Disclaimer
This software is a research prototype developed to demonstrate the feasibility of localized probabilistic encryption. While it has passed standard statistical tests, it should be reviewed thoroughly by security experts before being used in production environments for critical security applications.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
