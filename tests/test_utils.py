import pytest
import json
from unittest.mock import mock_open, patch

from src.category import Category
from src.product import Product
from src.utils import read_json, created_object_from_json


def test_read_json_success():
    """Создаем словарь с фиктивными данными"""
    fake_json = {
        "name": "Телефоны",
        "description": "Устройство, без которого жизнь немыслима",
        "products": "Xiaomi 15"
    }
    # Переводим словарь в строку
    fake_json_string = json.dumps(fake_json)

    # Подменям встренную функцию open с помощью mock.open
    with patch("builtins.open", mock_open(read_data=fake_json_string)):
    # Вызываем функцию
        result = read_json("test_path.json")

    # Проверка результата
    assert result == fake_json
    assert result["description"] == "Устройство, без которого жизнь немыслима"


def test_read_json_not_found():
    """Тестируем отсутствие json-файла"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_json("missing_path.json")


def test_created_object_json():
    """Тестируем создание объектов класса из json-файла"""
    # Подготовливаем тестовые данные
    mock_json_data = [
        {"name": "Телефоны",
         "description": "Устройство, без которого жизнь немыслима",
         "products": [
             {
             "name": "Xiaomi 15",
             "description": "Телефоны",
             "price": 80.0,
             "quantity": 7
             }
         ]
         }
    ]
    result = created_object_from_json(mock_json_data)

    assert len(result) == 1

    category = result[0]
    assert isinstance(category, Category)
    assert category.name == "Телефоны"
    assert "Xiaomi 15, 80.0 руб. Остаток 7 шт." in category.products
