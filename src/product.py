class Product:
    """Создаем класс Продукты"""
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


if __name__ == "__main__":  # pragma: no cover
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5)
    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8)
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)
