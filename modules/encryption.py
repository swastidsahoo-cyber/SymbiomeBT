"""
Cryptographic utilities for the Clinical Data Vault.
Ensures data is encrypted at rest using AES-256 (Fernet).
"""
from cryptography.fernet import Fernet
import os

class DataEncryption:
    """Handles encryption and decryption of sensitive health data."""
    
    def __init__(self, key: bytes = None):
        # In a real app, this key would be stored in environment variables or a HSM
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
        
    def encrypt_data(self, data: str) -> str:
        """Encrypts a string and returns the ciphertext."""
        return self.cipher.encrypt(data.encode()).decode()
        
    def decrypt_data(self, token: str) -> str:
        """Decrypts a token and returns the original string."""
        return self.cipher.decrypt(token.encode()).decode()

    def get_key_string(self) -> str:
        """Returns the key as a string for storage/export."""
        return self.key.decode()
