import pytest

from src.product import Product
from src.smartphone import Smartphone


def test_smartphone_init(smartphone_exemplar):
    """Тестируем инициализацию класса Smartphone"""
    assert smartphone_exemplar.name == "Samsung Galaxy S23 Ultra"
    assert smartphone_exemplar.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone_exemplar.price == 180000.0
    assert smartphone_exemplar.quantity == 5
    assert smartphone_exemplar.efficiency == 95.5
    assert smartphone_exemplar.model == "S23 Ultra"
    assert smartphone_exemplar.memory == 256
    assert smartphone_exemplar.color == "Серый"


def test_smartphone_inheritance():
    """Тестриуем, что класс Смартфоны является наследником класса Продукты"""
    assert issubclass(Smartphone, Product)


def test_smartphone_add_successful(smartphone_exemplar):
    """Тестцруем успешное сложение двух объектов класса Смартфоны"""
    other_smartphone = Smartphone(name="Iphone 15",
                                  description="512GB, Gray space",
                                  price=210000.0,
                                  quantity=8,
                                  efficiency=98.2,
                                  model="15",
                                  memory=512,
                                  color="Gray space")
    expected_result = (smartphone_exemplar.price * smartphone_exemplar.quantity) + \
                      (other_smartphone.price * other_smartphone.quantity)
    assert smartphone_exemplar + other_smartphone == expected_result


def test_smartphone_add_error(smartphone_exemplar, lawngrass_exemplar):
    """Тестируем ошибку при сложении экземпляров класса с продуктами другого класса"""
    with pytest.raises(TypeError):
        smartphone_exemplar + lawngrass_exemplar
