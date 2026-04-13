import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функция принимает список словарей и строку для поиска и возвращает
    список словарей, в котором есть указанная строка"""
    return [d for d in data if re.findall(search, d.get("description", ""), flags=re.IGNORECASE)]


def process_bank_operations(data: list[dict], category: list) -> dict:
    """Функция принимает список словарей с данными о банковских операциях
    и список категорий операций, и возвращает словарь, где ключи - это название категорий,
     а значения - количество операций в каждой категории"""
    result = {cat: 0 for cat in category}  # Создаем словарь, где для каждой категории из списка изначально задан 0
    list_category = [d["category"] for d in data]  # Создаем новый список, содержащий только категории
    counted = Counter(list_category)  # Подсчитываем количество каждой категории
    for category in result:
        if category in counted:
            result[category] = counted[category]
    return result


if __name__ == "__main__":  # pragma: no cover
    result_1 = [{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572",
                 "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                 "description": "Перевод организации", "from": "Счет 75106830613657916952",
                 "to": "Счет 11776614605963066702"},
                {"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878",
                 "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                 "description": "Перевод со счета на счет", "from": "Счет 19708645243227258542",
                 "to": "Счет 75651667383060284188"},
                {"id": 873106923, "state": "EXECUTED", "date": "2019-03-23T01:09:46.296404",
                 "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                 "from": "Счет 44812258784861134719", "to": "Счет 74489636417521191160"}]
    result_2 = [{"id": 1, "description": "Покупка продуктов", "category": "Супемаркеты", "amount": 100},
                {"id": 2, "description": "Оплата ЖКХ", "category": "Коммунальные услуги", "amount": 500},
                {"id": 3, "description": "Билеты в театр", "category": "Развлечения", "amount": 200},
                {"id": 3, "description": "Абонемент в фитнес", "category": "Развлечения", "amount": 400}]
    result_3 = ["Супемаркеты", "Коммунальные услуги", "Развлечения"]

    print(process_bank_search(result_1, search="Перевод"))
    print(process_bank_operations(result_2, result_3))
