import sys
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


import os


def is_db_file(file_path):
    """
    Проверяет, является ли выбранный файл файлом с расширением .db.

    :param file_path: Путь к файлу, который нужно проверить.
    :return: True, если файл имеет расширение .db, иначе False.
    """
    if not os.path.isfile(file_path):
        return False  # Не существует или это не файл
    _, extension = os.path.splitext(file_path)  # Разделяем имя файла и расширение
    return extension.lower() == '.db'

def get_path_db():
    choice = questionary.path("Choose a database file (press Tab):", file_filter=is_db_file).ask()
    if is_db_file(choice) != True:
        questionary.press_any_key_to_continue('No .db files have been found in the current directory. Press any key to '
                                              'quit').ask()
        sys.exit()
    else:
        return choice

def is_encrypted(note):
    if isinstance(note, bytes):
        return True




    # current_path = os.getcwd()
    #     while True:
    #         # Получить список файлов и папок
    #         items = [".."] + os.listdir(current_path)
    #         selected = questionary.select(f"Текущая директория: {current_path}. Выберите файл или папку:",
    #             choices=items, ).ask()
    #
    #         if not selected:
    #             print("Выход из выбора.")
    #             break
    #
    #         selected_path = os.path.join(current_path, selected)
    #
    #         # Если выбран файл, завершить выбор
    #         if os.path.isfile(selected_path):
    #             return selected_path
    #         # Если выбрана директория, изменить текущий путь
    #         elif os.path.isdir(selected_path):
    #             current_path = os.path.abspath(selected_path)
    #         else:
    #             print("Выбрано неверное значение.")


# data = "Hello, World!"
# binary_data = data.encode('utf-8')  # Перевод строки в бинарный вид
# binary_data = "Hello, World!"
# check_field_type(binary_data)
# print('go on')

