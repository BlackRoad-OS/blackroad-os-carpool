"""
Cryptography Utilities

AES-256-GCM encryption for API keys and sensitive data.
Per 02-ARCHITECTURE.md
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64


class EncryptionService:
    """
    AES-256-GCM encryption service for sensitive data.

    Used for:
    - API keys
    - OAuth tokens
    - Other secrets
    """

    def __init__(self, master_key: str):
        """
        Initialize encryption service.

        Args:
            master_key: Master encryption key from env (ENCRYPTION_SECRET)
        """
        # Derive a 256-bit key from master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"blackroad-os-salt",  # Static salt for deterministic key
            iterations=100000,
        )
        self.key = kdf.derive(master_key.encode())
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, plaintext: str) -> tuple[str, str]:
        """
        Encrypt plaintext.

        Args:
            plaintext: Data to encrypt

        Returns:
            Tuple of (encrypted_data, iv) both base64-encoded
        """
        # Generate random IV
        iv = os.urandom(12)

        # Encrypt
        ciphertext = self.aesgcm.encrypt(
            iv,
            plaintext.encode(),
            None  # No additional data
        )

        # Base64 encode for storage
        encrypted_b64 = base64.b64encode(ciphertext).decode()
        iv_b64 = base64.b64encode(iv).decode()

        return encrypted_b64, iv_b64

    def decrypt(self, encrypted_data: str, iv: str) -> str:
        """
        Decrypt data.

        Args:
            encrypted_data: Base64-encoded ciphertext
            iv: Base64-encoded initialization vector

        Returns:
            Decrypted plaintext

        Raises:
            cryptography.exceptions.InvalidTag: If decryption fails
        """
        # Decode from base64
        ciphertext = base64.b64decode(encrypted_data)
        iv_bytes = base64.b64decode(iv)

        # Decrypt
        plaintext = self.aesgcm.decrypt(iv_bytes, ciphertext, None)

        return plaintext.decode()


def get_encryption_service() -> EncryptionService:
    """
    Get encryption service singleton.

    Uses ENCRYPTION_SECRET from environment.
    """
    encryption_secret = os.getenv("ENCRYPTION_SECRET")
    if not encryption_secret:
        raise ValueError("ENCRYPTION_SECRET not set")

    return EncryptionService(encryption_secret)
