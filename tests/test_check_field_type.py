from app.functions import is_encrypted


def test_str_type():
    assert is_encrypted("12a12b2024") == False

data = "Hello, World!"
binary_data = data.encode('utf-8')
def test_BLOB_type():
    assert is_encrypted(binary_data) == True

