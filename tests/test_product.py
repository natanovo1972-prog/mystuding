from src.product import Product
from tests.conftest import product_exemplar


def test_product_init(product_exemplar):
    """Тестируем инициализацию экземпляров класса Продукты"""
    assert product_exemplar.name == "Samsung Galaxy S23 Ultra"
    assert product_exemplar.description == "256GB, Серый цвет, 200MP камера"
    assert product_exemplar.price == 180000.0
    assert product_exemplar.quantity == 5


def test_new_product():
    """Тестируем создание продукта через класс-метод new_product"""
    product_data = {
        "name": "Samsung",
        "description": "Смартфон",
        "price": 80000.0,
        "quantity": 5
    }
    product_new = Product.new_product(product_data)
    assert product_new.name == "Samsung"
    assert product_new.description == "Смартфон"
    assert product_new.price == 80000.0
    assert product_new.quantity == 5


def test_price_setter(product_exemplar):
    """Тестируем изменение цены через сеттер"""
    product_exemplar.price = 15000.0
    assert product_exemplar.price == 15000.0

    product_exemplar.price = -15000.0
    assert product_exemplar.price == 15000.0
