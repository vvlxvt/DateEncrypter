import copy
from db_handler import ConnectDB
from functions import get_path_db, encrypt_data, decrypt_data
import questionary
import sys
def crypt_func(db):
    table = db.get_tables()

    choice = questionary.select("Выберите: ", choices=['зашифровать', 'дешифровать', 'Выйти']).ask()
    if choice == 'зашифровать':
        process_data = encrypt_data
        message = "Пароли успешно зашифрованы!"
    elif choice == "дешифровать":
        process_data = decrypt_data
        message = "Пароли успешно расшифрованы!"
    elif choice == "Выйти":
        message = "Выход из программы."
        sys.exit()  # Завершает выполнение программы

    db.connect()
    query_fields = f'PRAGMA table_info({table})'
    fields = db.execute_query(query_fields)
    cleaned_fields = [x[1] for x in fields]
    choice_fields = questionary.select("Выберите поле для шифрования:", choices=cleaned_fields).ask()
    field = copy.deepcopy(choice_fields)

    query = f'SELECT name, {field} FROM {table}'
    notes = db.execute_query(query)

    key = input(f'введите ключ чтобы {choice}: ')

    for name, column in notes:
        processed_password = process_data(column, key)
        update_query = f'UPDATE {table} SET {field} = ? WHERE name = ?'
        db.execute_query(update_query, (processed_password, name))
    print(message)

    db.close()

# Пример использования:
if __name__ == "__main__":
    db_path = get_path_db()
    db = ConnectDB(db_path)
    crypt_func(db)





