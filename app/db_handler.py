import sqlite3
from pathlib import Path
import questionary

class ConnectDB:
    def __init__(self, db_path):
        """
        Инициализация класса с указанием пути к базе данных.
        :param db_path: Путь к файлу базы данных.
        """
        self.db_path = Path(db_path)
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            # print(f"Успешно подключено к базе данных: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            raise

    def execute_query(self, query, params=None):
        """
        Выполняет SQL-запрос.
        :param query: SQL-запрос для выполнения.
        :param params: Параметры для подстановки в запрос.
        :return: Результаты запроса, если это SELECT; иначе None.
        """
        if not self.cursor:
            raise ConnectionError("Сначала установите соединение с базой данных с помощью метода connect().")
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

    def test_query(self, query, params=None):
        self.cursor.execute("BEGIN TRANSACTION")
        try:
            self.cursor.execute(query, params)
            # Если всё корректно, просто отмените транзакцию
            self.cursor.execute("ROLLBACK")
            print('все ОК')
        except sqlite3.OperationalError as e:
            print(f"Ошибка выполнения запроса: {e}")
            self.cursor.execute("ROLLBACK")
            print('недопустимая операция')


    def close(self):
        # Закрывает соединение с базой данных.
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
