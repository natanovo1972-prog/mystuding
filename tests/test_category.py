from src.category import Category


def test_category_init(category_exemplar):
    """Тестируем инициализацию экземпларов класса Категории"""
    assert category_exemplar.name == "Смартфоны"
    assert category_exemplar.description == (
        "Смартфоны, как средство не только коммуникации,"
        "но и получения дополнительных функций для удобства жизни"
    )
    assert len(category_exemplar.products) == 2


def test_category_count(category_exemplar, category_attribute):
    """Тестируем, что счетчики класса правильно суммируют данные двух атрибутов"""
    assert Category.category_count == 2
    assert Category.product_count == 5
