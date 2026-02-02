# KILIM-Cipher: Probabilistic Stream Cipher with Native Turkish Support for IoT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/1147470580.svg)](https://doi.org/10.5281/zenodo.18452264)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange.svg)]()

**KILIM** is a novel probabilistic stream cipher designed to provide robust security for localized character sets, specifically optimizing for **Turkish language support** in resource-constrained IoT environments.

This repository contains the reference implementation and the graphical user interface (GUI) for the research paper:
> **"A Probabilistic Stream Cipher with Native Turkish Support for IoT"**
> *Submitted to the Journal of Information Security and Applications (JISA)*.

---

## 🧶 What is KILIM?

The name **KILIM** is twofold:

1.  **Technical Acronym:** It stands for **K**eyed **I**ndex **L**inked **I**ntegrity **M**echanism.
2.  **Cultural Metaphor:** In Turkish culture, a *"Kilim"* is a traditional woven rug. Just as a Kilim is woven loop by loop, this algorithm weaves each character into the encryption stream using a **Dynamic Index Chaining** mechanism. The state of each character depends on the entire history of the weaving process, ensuring that no pattern is repeated.

---

## 🚀 Key Features

* **High Performance:** Benchmarked at **0.13 seconds** per 1 MB encryption with **O(n)** complexity, making it ~6x faster than pure Python RC4 implementations.
* **IoT Optimized:** Extremely low memory footprint (~9.5 KB for table structures), ideal for microcontrollers.
* **Native Turkish Support:** Operates on an expanded character pool ($N=269$), natively supporting characters like `ç, ğ, ı, ö, ş, ü` without encoding overhead.
* **Probabilistic Encryption:** Utilizing HMAC-SHA256 for dynamic table seeding, ensuring that the same plaintext results in different ciphertexts in every session.
* **Dynamic Index Chaining:** Features a state-dependent indexing mechanism ($I_k$) that links each character encryption to the entire preceding stream, mitigating frequency analysis.
* **Verified Randomness:** The algorithm successfully passes **NIST STS** and **Dieharder** statistical randomness tests.

---

## 📊 Performance Benchmarks

The algorithm was tested on a standard Python 3.10 environment (Intel i7-1165G7).

| Metric | Value |
| :--- | :--- |
| **1 MB Encryption Time** | **0.13 seconds** |
| **Avg Encryption (1 KB)** | **0.21 ms** |
| **Memory Usage** | **~8.8 KB** |
| **Complexity** | **Linear O(n)** |

---

### ⚡ Real-World Speed Test (Terminal Output)
Below is the output from our comparative benchmark script (`benchmark_ultimate.py`), demonstrating KILIM's advantage over legacy stream ciphers in a pure software environment:

```text
============================================================
ULTIMATE BENCHMARK: 1 MB DATA (Avg of 10 runs)
============================================================
RC4 (Python Legacy) : 0.81455 s
KILIM (Proposed)    : 0.13470 s  <-- (Over 6x Faster)
AES-256 (Hardware)  : 0.01635 s
ChaCha20 (C-Lib)    : 0.00235 s
------------------------------------------------------------
```

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

---

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

---

### 🛡️ Summary of Results
The algorithm passed **all 15 tests** in the NIST Statistical Test Suite (STS 2.1.2) and the **Dieharder** battery of tests with a significance level of $\alpha = 0.01$.

| Test Suite | Result | Key Metrics (P-Values) |
| :--- | :--- | :--- |
| **NIST STS (15/15)** | **✅ PASSED** | Monobit: `0.5431` \| Runs: `0.6183` \| FFT: `0.7399` |
| **Dieharder** | **✅ PASSED** | DNA: `0.0618` \| Birthdays: `0.3625` \| Bitstream: `0.9153` |

<details>
<summary><b>🔍 Click to see NIST Test Log Snippet</b></summary>

```text
------------------------------------------------------------------------------
RESULTS FOR THE UNIFORMITY OF P-VALUES AND THE PROPORTION OF PASSING SEQUENCES
------------------------------------------------------------------------------
   generator is <data/nist_large_output.bin>
------------------------------------------------------------------------------
 C1  C2  C3  C4  C5  C6  C7  C8  C9  C10  P-VALUE  PROPORTION  STATISTICAL TEST
------------------------------------------------------------------------------
  9   9   8  11  12   8  11   7  12  13  0.534146    100/100     Frequency
 12   7  13   9   8  10   8  13  11   9  0.739918    100/100     BlockFrequency
  8  10  11   9  12   9  11  10  10  10  0.122325    100/100     Runs
 10  12   9  10   9  11   8  10  11  10  0.739918    100/100     FFT
 ...
------------------------------------------------------------------------------
```
The minimum pass rate for each statistical test with the exception of the
random excursion (variant) test is approximately = 96 for a
sample size = 100 binary sequences.

For further details, see [RESULTS](https://github.com/hlmclgl/KILIM-Cipher/tree/main/results)
</details>

---

## ⚠️ Disclaimer
This software is a research prototype developed to demonstrate the feasibility of localized probabilistic encryption. While it has passed standard statistical tests, it should be reviewed thoroughly by security experts before being used in production environments for critical security applications.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/hlmclgl/KILIM-Cipher/blob/main/LICENSE) file for details.
