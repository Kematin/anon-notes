import os

from cryptography.fernet import Fernet, InvalidToken

from config import BASE_DIR
from exceptions import CryptoException

__default_secret_key = f"{BASE_DIR}/secret.key"


def get_secret_key(filename: str) -> str:
    if not os.path.isfile(filename):
        raise CryptoException("No key was provided.")
    return open(filename).read()


def encrypt_content(text: str, key: str = __default_secret_key) -> bytes:
    key = get_secret_key(key)
    f = Fernet(key)
    data = str.encode(text)
    token = f.encrypt(data)
    return token


def decrypt_content(data: bytes, key: str = __default_secret_key) -> str:
    key = get_secret_key(key)
    f = Fernet(key)
    try:
        text_data = f.decrypt(data)
    except InvalidToken:
        raise CryptoException("Invalid key pair token.")
    return text_data.decode()
