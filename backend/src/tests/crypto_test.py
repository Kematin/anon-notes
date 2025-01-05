import os

import pytest
from cryptography.fernet import Fernet

from exceptions import CryptoException
from service.crypto import (
    decrypt_content,
    encrypt_content,
    get_secret_key,
)

TEST_SECRET_KEY_FILE = "test_secret.key"
TEST_SECOND_SECRET_KEY_FILE = "test_secret2.key"


@pytest.fixture(scope="module", autouse=True)
def generate_test_secret_key():
    key = Fernet.generate_key()
    with open(TEST_SECRET_KEY_FILE, "wb") as file:
        file.write(key)

    key = Fernet.generate_key()
    with open(TEST_SECOND_SECRET_KEY_FILE, "wb") as file:
        file.write(key)

    yield

    os.remove(TEST_SECRET_KEY_FILE)
    os.remove(TEST_SECOND_SECRET_KEY_FILE)


def test_get_secret_key():
    key = get_secret_key(TEST_SECRET_KEY_FILE)
    assert isinstance(key, str)
    assert len(key) > 1


def test_get_secret_key_fail():
    with pytest.raises(CryptoException, match="No key was provided."):
        get_secret_key("nonexist.key")


def test_encrypt_and_decrypt():
    test_text = "Test!"
    encrypted = encrypt_content(test_text, key=TEST_SECRET_KEY_FILE)
    decrypted = decrypt_content(encrypted, key=TEST_SECRET_KEY_FILE)
    assert decrypted == test_text


def test_invalid_key_pairs():
    test_text = "Test!"
    encrypted = encrypt_content(test_text, key=TEST_SECRET_KEY_FILE)
    with pytest.raises(CryptoException, match="Invalid key pair token."):
        decrypt_content(encrypted, key=TEST_SECOND_SECRET_KEY_FILE)


def test_encrypt_with_invalid_file():
    os.remove(TEST_SECRET_KEY_FILE)
    with pytest.raises(CryptoException, match="No key was provided."):
        encrypt_content("This should fail.", key=TEST_SECRET_KEY_FILE)

    with open(TEST_SECRET_KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())
