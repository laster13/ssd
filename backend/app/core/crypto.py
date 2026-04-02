from cryptography.fernet import Fernet
from app.core.config import settings

fernet = Fernet(settings.totp_encryption_key.encode())


def encrypt_secret(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()


def decrypt_secret(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()