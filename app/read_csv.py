import sqlite3
import csv
from pathlib import Path

# Пути к файлу CSV и базе данных
csv_file = Path(__file__).parent.parent / "db" / "pk_backup_2025-01-09.csv"
db_file = Path(__file__).parent.parent / "db" / "my_database.db"
# db_file = 'db/my_database.db'

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Чтение заголовков (первая строка)

    # Создание таблицы с динамическими столбцами
    columns = ', '.join([f'"{header}" TEXT' for header in headers])
    cursor.execute(f'CREATE TABLE IF NOT EXISTS my_table ({columns})')


    cursor.executemany(f'INSERT INTO my_table VALUES ({", ".join(["?"] * len(headers))})', reader)


conn.commit()
conn.close()

print("Данные успешно импортированы!")
