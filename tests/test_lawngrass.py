from src.lawngrass import LawnGrass
from src.product import Product


def test_lawngrass_init(lawngrass_exemplar):
    """Тест на инициализацию класса Газонная трава"""
    assert lawngrass_exemplar.name == "Газонная трава"
    assert lawngrass_exemplar.description == "Элитная трава для газона"
    assert lawngrass_exemplar.price == 500.0
    assert lawngrass_exemplar.quantity == 20
    assert lawngrass_exemplar.country == "Россия"
    assert lawngrass_exemplar.germination_period == "7 дней"
    assert lawngrass_exemplar.color == "Зеленый"


def test_lawngrass_inheritance():
    """Тестируем, что класс Газонная трава является наследником класса Продукты"""
    assert issubclass(LawnGrass, Product)


def test_add_lawngrass_successful(lawngrass_exemplar):
    """Тестируем успешное сложение экземпляров класса Газонная трава"""
    other_lawngrass = LawnGrass(name="Газонная трава 2",
                                description="Выносливая трава",
                                price=450.0,
                                quantity=15,
                                country="США",
                                germination_period="5 дней",
                                color="Темно-зеленый")
    expected_result = (lawngrass_exemplar.price * lawngrass_exemplar.quantity) + \
                      (other_lawngrass.price * other_lawngrass.quantity)
    assert lawngrass_exemplar + other_lawngrass == expected_result
