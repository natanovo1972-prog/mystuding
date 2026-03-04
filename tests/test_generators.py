import re

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize("input_transaction, currency, expected_result", [
    # Тест: значение currency = USD
    ([{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572",
       "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод организации", "from": "Счет 75106830613657916952",
       "to": "Счет 11776614605963066702"},
      {"id": 873106923, "state": "EXECUTED", "date": "2019-03-23T01:09:46.296404",
       "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
       "description": "Перевод со счета на счет", "from": "Счет 44812258784861134719",
       "to": "Счет 74489636417521191160"}], "USD",
     [{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572",
       "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод организации", "from": "Счет 75106830613657916952",
       "to": "Счет 11776614605963066702"}])])
def test_filter_by_currency(input_transaction: list, currency: str, expected_result: list) -> None:
    result = filter_by_currency(input_transaction, currency)
    assert list(result) == expected_result


@pytest.mark.parametrize("input_transaction, currency, expected_result", [
    # Тест: значение currency не соответствует USD
    ([{"id": 873106923, "state": "EXECUTED", "date": "2019-03-23T01:09:46.296404",
       "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
       "description": "Перевод со счета на счет", "from": "Счет 44812258784861134719",
       "to": "Счет 74489636417521191160"}], "USD", [])])
def test_filter_by_currency_invalid(input_transaction: list, currency: str, expected_result: list) -> None:
    result_invalid = filter_by_currency(input_transaction, currency)
    assert list(result_invalid) == expected_result


def test_filter_by_currency_empty(transaction_empty: list) -> None:
    # Тест: на вход подается пустой список
    result = filter_by_currency(transaction_empty, "USD")
    assert list(result) == []


def test_filter_by_invalid_currency(transaction_no_currency: list) -> None:
    # Тест: на вход подается список без ожидаемых валютных значений
    result = filter_by_currency(transaction_no_currency, "USD")
    assert list(result) == []


def test_transaction_description(transaction_description_valid: list) -> None:
    result = transaction_descriptions(transaction_description_valid)
    assert next(result) == "Перевод организации"
    assert next(result) == "Перевод со счета на счет"
    assert next(result) == "Перевод со счета на счет"
    assert next(result) == "Перевод с карты на карту"
    assert next(result) == "Перевод организации"


def test_transaction_descriptions_empty(transaction_empty: list) -> None:
    # Тестируем пустой список транзакций
    result = transaction_descriptions(transaction_empty)
    assert list(result) == []


@pytest.mark.parametrize("input_transaction, expected_result", [
    # Тестируем одну транзакцию
    ([{"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878",
       "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод со счета на счет", "from": "Счет 19708645243227258542",
       "to": "Счет 75651667383060284188"}], ["Перевод со счета на счет"])])
def test_one_transaction_description(input_transaction: list, expected_result: list) -> None:
    result = transaction_descriptions(input_transaction)
    assert list(result) == expected_result


def test_card_number_generator() -> None:
    # Тестируем, что итератор правильно формирует номера карт
    generator_1 = card_number_generator(4, 5)
    generator_2 = card_number_generator(45556, 45557)
    assert next(generator_1) == "0000 0000 0000 0004"
    assert next(generator_1) == "0000 0000 0000 0005"
    assert next(generator_2) == "0000 0000 0004 5556"
    assert next(generator_2) == "0000 0000 0004 5557"


def test_card_number_generator_invalid() -> None:
    # Тестируем корректность формата карты
    start, stop = 1, 5
    gen = card_number_generator(start, stop)
    card_format = r"^\d{4} \d{4} \d{4} \d{4}$"
    for card_number in gen:
        assert re.match(card_format, card_number) is not None, f"Ошибка в формате: {card_number}"


def test_card_number_generator_final() -> None:
    # Тест на обработку крайних значений диапозона
    start, stop = 3, 5
    gen = card_number_generator(start, stop)
    assert next(gen) == "0000 0000 0000 0003"
    next(gen)
    assert next(gen) == "0000 0000 0000 0005"
    with pytest.raises(StopIteration):
        next(gen)
