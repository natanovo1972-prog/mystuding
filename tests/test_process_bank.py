import pytest

from src.process_bank import process_bank_search, process_bank_operations


@pytest.mark.parametrize(
    "data, search, result",
    [
        (
            [{"id": 1, "describtion": "Покупки в супермаркетах"}],
            "Покупки",
            [{"id": 1, "describtion": "Покупки в супермаркетах"}],
        ),
        (
            [{"id": 2, "describtion": "Покупки на маркетплейсах"}],
            "Покупки",
            [{"id": 2, "describtion": "Покупки на маркетплейсах"}],
        ),
        ([{"id": 3, "describtion": ""}], "Покупки", []),
    ],
)
def test_process_bank_search_success(data, search, result):
    assert process_bank_search(data, search) == result


def test_process_bank_search_found(search_string):
    # Поиск существующей строки без учета регистра
    search_word = "покупки"
    result = process_bank_search(search_string, search_word)
    for item in result:
        assert search_word.lower() in item["description"].lower()


def test_process_bank_search_not_found(search_string):
    # Поиск строки, которая не указана в данных
    result = process_bank_search(search_string, "зарплата")
    assert result == []


def test_process_bank_search_empty_list():
    # Поиск в пустом списке
    result = process_bank_search([], "")
    assert result == []


@pytest.mark.parametrize(
    "data, category, result",
    [
        (
            [
                {"id": 1, "describtion": "Продукты в супермаркетах", "category": "Продукты"},
                {"id": 2, "describtion": "Продукты на рынке", "category": "Продукты"},
            ],
            ["Продукты", "Еда"],
            {"Продукты": 2},
        )
    ],
)
def test_process_bank_operations_success(data, category, result):
    assert process_bank_operations(data, category) == result


def test_process_bank_operations_count(count_category):
    # Тестируем корректный подсчет операций в каждой категории
    category = ["Покупки", "Перевод", "Оплата"]
    result = {"Покупки": 2, "Перевод": 1, "Оплата": 1}
    assert process_bank_operations(count_category, category) == result


def test_process_bank_operations_no_match(non_matching):
    # Тестируем несовпадение описания с категориями
    category = ["Покупки", "Перевод", "Оплата"]
    expected_result = {"Покупки": 0, "Перевод": 0, "Оплата": 0}
    result = process_bank_operations(non_matching, category)
    assert result == expected_result


def test_process_bank_operations_empty(empty_data):
    # Тестируем пустой список словарей
    category = ["Покупки", "Перевод", "Оплата"]
    result = process_bank_operations(empty_data, category)
    assert result == {}
