import pytest

from src.product import Product
from src.category import Category


@pytest.fixture
def product_exemplar():
    """Фикстура для тестирования экземпляра класса Продукты"""
    return Product(name="Samsung Galaxy S23 Ultra",
                   description="256GB, Серый цвет, 200MP камера",
                   price=180000.0,
                   quantity=5
                   )


@pytest.fixture
def category_exemplar():
    """Фикстура для тестирования экземпляра класса Категории"""
    return Category(name="Смартфоны",
                    description="Смартфоны, как средство не только коммуникации,"
                                "но и получения дополнительных функций для удобства жизни",
                    products=[
                        Product(
                            "Iphone 15",
                            "512GB, Gray space",
                            210000.0,
                            8),
                        Product(
                            "Xiaomi Redmi Note 11",
                            "1024GB, Синий",
                            31000.0,
                            14)
                    ]
                    )


@pytest.fixture
def category_attribute():
    """Фикстура для тестирования атрибутов класса Категории"""
    return Category(name="Смартфоны",
                    description="Смартфоны, как средство не только коммуникации,"
                                "но и получения дополнительных функций для удобства жизни",
                    products=[
                        Product(
                            "Samsung Galaxy S23 Ultra",
                            "256GB, Серый цвет, 200MP камера",
                            180000.0,
                            5),
                        Product(
                            "Iphone 15",
                            "512GB, Gray space",
                            210000.0,
                            8),
                        Product(
                            "Xiaomi Redmi Note 11",
                            "1024GB, Синий",
                            31000.0,
                            14)
                    ]
                    )


@pytest.fixture(autouse=True)
def clean_counters():
    """Эта фикстура автоматически очищает счетчики перед КАЖДЫМ тестом"""
    Category.category_count = 0
    Category.product_count = 0
