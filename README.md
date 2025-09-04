# KryptBoard Emulator

KryptBoard is a simple Python desktop application that emulates a keyboard with live ChaCha20-Poly1305 encryption of the typed text. It provides a visual virtual keyboard that highlights keys on real keypress and displays both the plaintext and the live encrypted output (nonce, ciphertext, and tag in base64). [9]

## Features
- Plaintext Output: Displays the characters typed in real-time. [10]
- Encrypted Output: Shows live ChaCha20-Poly1305 output with base64-encoded nonce, ciphertext, and tag; each keypress re-encrypts using a fresh 12-byte nonce and the current 32-byte session key. [9]
- Virtual Keyboard: Visual QWERTY keyboard highlights keys on physical keypress and release. [10]
- Send (plaintext) Button: Prints current plaintext to the console and clears the plaintext area. [10]
- Send (encrypted) Button: Prints nonce, ciphertext, and tag (base64) to the console and clears both areas. [9]
- Reset Key Button: Generates a new random 32-byte key and clears both output areas. [9]

## Requirements
- Python 3.10+ (Tkinter is included with most official installers). [11]
- pycryptodome for ChaCha20-Poly1305. [12]

## Setup
1. Clone and enter the project directory. [13]
   ```
   git clone <repo-url>
   cd KryptBoard-Emulator
   ```
2. Create and activate a virtual environment (Windows). [14]
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies. [11][12]
   ```
   python -m pip install --upgrade pip wheel setuptools
   python -m pip install pycryptodome
   ```
4. Optional: self-test crypto install. [11]
   ```
   python -m Crypto.SelfTest
   ```

## Run
```
python app.py
```
[11]

## Usage
- Type in the plaintext area; the encrypted panel updates each keystroke with a fresh 12-byte nonce and the ChaCha20-Poly1305 ciphertext and tag, all base64-encoded. [9]
- Send (plaintext) prints and clears plaintext; Send (encrypted) prints a JSON-like triple (nonce, ciphertext, tag) and clears both areas. [9]
- Reset Key generates a new random 32-byte key and clears outputs; subsequent keystrokes encrypt under the new key. [9]

## Security notes
- Key: 32 bytes required by ChaCha20-Poly1305; generated via a secure RNG. [9]
- Nonce: 12 bytes, must be unique per key. A random nonce per keystroke avoids reuse. [9]
- Tag: The authentication tag verifies integrity and authenticity; keep ciphertext and tag together. [9]

## Troubleshooting
- ModuleNotFoundError: No module named 'Crypto' → activate the venv and install into it:
  ```
  python -m pip install pycryptodome
  python -c "from Crypto.Random import get_random_bytes; print(len(get_random_bytes(16)))"
  ```
  [11][12]
- Tkinter not found (minimal Linux installs) → install system Tk packages, then ensure Python’s Tk bindings are available. [11]
- Crypto self-test fails → remove legacy PyCrypto and reinstall pycryptodome:
  ```
  python -m pip uninstall -y pycrypto crypto
  python -m pip install pycryptodome
  ```
  [11]

## Implementation details
- Encryption: ChaCha20-Poly1305 with 32-byte key and 12-byte nonce; `encrypt_and_digest` returns `(ciphertext, tag)`. [9]
- Nonce policy: Random 12-byte nonce per keystroke to avoid reuse; XChaCha20-Poly1305 (24-byte nonce) is also available if needed. [9]
- Event handling: Key press/release bound via Tkinter; highlight virtual keys on `<KeyPress>`/`<KeyRelease>`. [10][15]

## Example (core crypto)
```
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
import base64

key = get_random_bytes(32)              # 32-byte key
nonce = get_random_bytes(12)            # 12-byte nonce
cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(b"hello")
out = {
    "nonce": base64.b64encode(nonce).decode(),
    "ciphertext": base64.b64encode(ciphertext).decode(),
    "tag": base64.b64encode(tag).decode(),
}
print(out)
```
[9]

## License
Add the project’s license here (e.g., MIT), and include a LICENSE file in the repo root. [13]

## Acknowledgments
Built with Tkinter and pycryptodome’s ChaCha20-Poly1305 implementation. [12][9]
```