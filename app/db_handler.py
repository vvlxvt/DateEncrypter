import sqlite3
from pathlib import Path
import questionary

class ConnectDB:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            raise

    def execute_query(self, query, params=None):

        if not self.cursor:
            raise ConnectionError("Сначала установите соединение с базой данных.")
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if query.startswith("SELECT") or query.startswith("PRAGMA"):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            raise


    def close(self):
        if self.connection:
            self.connection.close()

    def get_tables(self):
        self.connect()
        try:
            # Получение списка таблиц
            tables: list = self.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
            cleaned_tables = [x[0] for x in tables] # очищаем список таблиц от лишних членов
        except Exception as e:
            print(f"Ошибка: {e}")
        choice = questionary.select("The following tables were found. Choose any one:",choices=cleaned_tables).ask()
        self.close()
        return choice
