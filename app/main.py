import copy
from db_handler import ConnectDB
from functions import get_path_db, encrypt_data, decrypt_data, is_encrypted
import questionary
import sys
def crypt_func(db):
    table = db.get_tables()

    choice = questionary.select("Make a choice: ", choices=['encrypt', 'decrypt', 'quit']).ask()
    if choice == 'encrypt':
        process_data = encrypt_data
        message = "Passwords have been successfully encrypted!"
    elif choice == "decrypt":
        process_data = decrypt_data
        message = "Passwords have been successfully decrypted!"
    elif choice == "quit":
        message = "Quit"
        sys.exit()

    db.connect()
    query_fields = f'PRAGMA table_info({table})'
    fields = db.execute_query(query_fields)
    cleaned_fields = [x[1] for x in fields]
    choice_fields = questionary.select(f"Choose a field to {choice}:", choices=cleaned_fields).ask()
    field = copy.deepcopy(choice_fields)

    query = f'SELECT name, {field} FROM {table}'
    notes = db.execute_query(query)
    if (is_encrypted(notes[0][1]) == True and choice == 'encrypt') or (is_encrypted(notes[0][1]) != True and choice ==
                                                                       'decrypt'):
        questionary.press_any_key_to_continue('need to change the method to the opposite one. Press any key to quit').ask()
        sys.exit()


    key = questionary.password(f"Input a key to {choice} data:").ask()

    for name, column in notes:
        processed_password = process_data(column, key)
        update_query = f'UPDATE {table} SET {field} = ? WHERE name = ?'
        db.execute_query(update_query, (processed_password, name))
    print(message)

    db.close()

if __name__ == "__main__":
    db_path = get_path_db()
    db = ConnectDB(db_path)
    crypt_func(db)





