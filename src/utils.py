import json
import os

from src.product import Product
from src.category import Category


def read_json(path: str) -> dict:
    """Функция для чтения файла JSON"""
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def created_object_from_json(data):
    """Функция создает объекты классов из JSON-файла"""
    categories = []
    for category in data:
        products = []
        for product in category["products"]:
            products.append(Product(**product))
        category["products"] = products
        categories.append(Category(**category))
    return categories


if __name__ == "__main__":  # pragma: no cover
    data = read_json("../data/products.json")
    category_data = created_object_from_json(data)
    print(category_data)
