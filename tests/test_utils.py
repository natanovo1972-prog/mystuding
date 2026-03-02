from unittest.mock import mock_open, patch

from src.utils import fin_transaction


@patch('builtins.open', new_callable=mock_open, read_data='[{"name": "Ivan", "age": 35}]')
def test_utils_correct(mock_file):  # mock_file - объект, созданный mock_open
    """Проверяем корректность обработки JSON-файла и возвращение списка"""
    result = fin_transaction('./data/operations.json')
    expected = [{"name": "Ivan", "age": 35}]
    assert result == expected
    mock_file.assert_called_once_with('./data/operations.json', 'r', encoding='utf-8')


@patch('builtins.open', mock_open(read_data='not a json'))
def test_utils_wrong_file():
    """Проверяем обработку некорректного файла"""
    result = fin_transaction('wrong.json')
    assert result == []


@patch('builtins.open', mock_open(read_data='json-file not found'))
def test_utils_file_not_found():
    """Проверяем, что файл не найден"""
    result = fin_transaction('FileNotFoundError')
    assert result == []


@patch('builtins.open', mock_open(read_data='json-file is not list'))
def test_utils_not_list():
    """Проверяем, что файл не является списком"""
    result = fin_transaction('not_list.json')
    assert result == []
