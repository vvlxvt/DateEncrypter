# DataEncrypter
encrypts/decrypts the data in the selected database field 

## Requirements

- Python 3.8+
- cryptography - a package which provides cryptographic recipes and primitives
- questionary 2.x - library for effortlessly building command line interfaces
- pyinstaller - bundles a Python application and all its dependencies into a single package
- pytest

## Project structure

```plaintext
DataEncrypter/
├── app/
│   ├── db_handler.py    # a model to connect with database (SQLite)
│   ├── functions.py     # auxiliary functions (encryption)
│   ├── read_csv.py      # transfers csv data to db file
│   └── main.py          # running script
├── tests/
│   └── test_check_field_type.py  # testing type of data
└── requirements.txt     # dependency file for library installation
```
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/vvlxvt/DateEncrypter
    ```

2. Установите зависимости:
    ```bash
    pip install cryptography questionary pyinstaller pytest
    ```

## Запуск

Запустите приложение с помощью команды:
   ```bash
   python app/main.py
   ```
## Конфигурация

```markdown
- need to change fields SQL query if your database contains other fields
- encryption field is selected manually in the running application
- use read_csv.py to export your *.csv data to *.db SQLite file 
```
## Примеры использования

**Testing**

Run tests with pytest:

```bash
.venv\Scripts\activate.ps1
pytest -v tests\test_check_field_type.py
```

### Замечание
add __init.py__ in app/ for testing and delete for *.exe compilation due to pyinstaller can work unexpected

## Контакты

Если у вас есть вопросы, пишите на [vvlxvt@gmail.com](vvlxvt@gmail.com).