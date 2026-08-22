from src.category import Category


def test_category_init(category_exemplar):
    """Тестируем инициализацию экземпларов класса Категории"""
    assert category_exemplar.name == "Смартфоны"
    assert category_exemplar.description == (
        "Смартфоны, как средство не только коммуникации,"
        "но и получения дополнительных функций для удобства жизни"
    )
    assert "Iphone 15" in category_exemplar.products
    assert "Xiaomi Redmi Note 11" in category_exemplar.products


def test_category_count(category_exemplar, category_attribute):
    """Тестируем, что счетчики класса правильно суммируют данные двух атрибутов"""
    assert Category.category_count == 2
    assert Category.product_count == 5


def test_add_product(category_exemplar, product_exemplar):
    """Тестируем добавление нового продукта в категорию"""
    category_exemplar.add_product(product_exemplar)
    assert Category.product_count == 3
    assert "Samsung Galaxy S23 Ultra" in category_exemplar.products


def test_category_products_format(category_exemplar):
    """Тестируем, что свойства продукта выводятся в нужном формате"""
    expected_format = (
        "Iphone 15, 210000.0 руб. Остаток 8 шт.\n"
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток 14 шт."
    )
    assert category_exemplar.products == expected_format


def test_category_str(category_exemplar):
    """Тестируем количество экземпляров каждого продукта"""
    result = str(category_exemplar)
    assert result == "Смартфоны, количество продуктов 22 шт."
