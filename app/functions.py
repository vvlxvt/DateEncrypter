import questionary
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_key(password: str) -> bytes:
    salt = b'\x00' * 16  # Пример соли
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_data(data: str, password: str) -> bytes:
    key = generate_key(password)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Паддинг
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted_data

def decrypt_data(encrypted_data: bytes, password: str) -> str:
    iv = encrypted_data[:16]  # Первый 16 байт — это IV
    cipher_text = encrypted_data[16:]
    key = generate_key(password)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
    # Удаляем паддинг
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    original_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Логируем расшифрованные данные как байты
    try:
        return original_data.decode()  # Пытаемся декодировать как строку
    except UnicodeDecodeError as e:
        print(f"Ошибка при декодировании данных: {e}")
        return None


from pathlib import Path
import os

def get_path_db():
    choice = questionary.path("Выбор файла:").ask()
    return choice




