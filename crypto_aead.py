# crypto_aead.py
# This file contains the cryptographic helper functions.

import base64
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

def aead_encrypt(msg: bytes, key_bytes: bytes):
    """
    Encrypts a message using ChaCha20-Poly1305 with a fresh random nonce.

    Args:
        msg: The plaintext message as bytes.
        key_bytes: The 32-byte encryption key.

    Returns:
        A dictionary containing the base64 encoded nonce, ciphertext, and tag.
    """
    # Generate a fresh random 12-byte nonce for each encryption
    nonce = get_random_bytes(12)
    cipher = ChaCha20_Poly1305.new(key=key_bytes, nonce=nonce)

    # Encrypt and digest
    ciphertext, tag = cipher.encrypt_and_digest(msg)

    return {
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8"),
    }

def aead_decrypt(nonce_b64: str, ct_b64: str, tag_b64: str, key_bytes: bytes) -> bytes:
    """
    Decrypts a ChaCha20-Poly1305 ciphertext and verifies the tag.

    Args:
        nonce_b64: The base64 encoded nonce string.
        ct_b64: The base64 encoded ciphertext string.
        tag_b64: The base64 encoded tag string.
        key_bytes: The 32-byte encryption key.

    Returns:
        The decrypted plaintext as bytes.

    Raises:
        ValueError: If decryption or tag verification fails.
    """
    nonce = base64.b64decode(nonce_b64)
    ct = base64.b64decode(ct_b64)
    tag = base64.b64decode(tag_b64)

    cipher = ChaCha20_Poly1305.new(key=key_bytes, nonce=nonce)

    # Decrypt and verify
    try:
        plaintext = cipher.decrypt_and_verify(ct, tag)
        return plaintext
    except ValueError:
        # This exception is raised by PyCryptodome if the tag is invalid
        raise ValueError("Decryption failed: Invalid tag or ciphertext.")
