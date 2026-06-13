
def test_product_init(product_exemplar):
    """Тестируем инициализацию экземпляров класса Продукты"""
    assert product_exemplar.name == "Samsung Galaxy S23 Ultra"
    assert product_exemplar.description == "256GB, Серый цвет, 200MP камера"
    assert product_exemplar.price == 180000.0
    assert product_exemplar.quantity == 5
