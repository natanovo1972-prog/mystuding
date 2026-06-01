import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import create_greeting, main


@pytest.mark.parametrize(
    "date_str, expected_greeting",
    [
        ("2026-05-15 07:00:00", "Доброе утро"),
        ("2026-05-15 11:59:59", "Доброе утро"),
        ("2026-05-15 12:00:00", "Добрый день"),
        ("2026-05-15 17:59:59", "Добрый день"),
        ("2026-05-15 18:00:00", "Добрый вечер"),
        ("2026-05-15 23:59:59", "Добрый вечер"),
        ("2026-05-15 00:00:00", "Доброй ночи"),
        ("2026-05-15 03:59:59", "Доброй ночи"),
    ],
)
def test_create_greeting_successful(date_str, expected_greeting):
    """Тест на успешное выполнение приветствия"""
    assert create_greeting(date_str) == expected_greeting


def test_create_greeting_incorrect():
    """Тест на приветствие в случае введения некорректной даты"""
    assert create_greeting("2026-31-05 14:00") == "Здравствуйте"


# Создаем фикстуры для подмены данных из Excel-файла и файла user_settings.json
@pytest.fixture
def mock_cards_df():
    return pd.DataFrame({"Последние 4 цифры номера карты": ["1234"], "Сумма операции": [5500.00], "Кэшбэк": [55]})


@pytest.fixture
def mock_transactions_df():
    return pd.DataFrame(
        {
            "Дата платежа": ["2026-05-15"],
            "Последние 4 цифры номера карты": ["1234"],
            "Сумма операции": [5500],
            "Категория": ["Одежда"],
            "Описание": ["Покупка пальто"],
        }
    )


@pytest.fixture
def fake_settings_json():
    return json.dumps(
        {
            "USDRUB": "91.50",
            "EURRUB": "99.20",
            "AAPL": 175.50,
            "AMZN": 180.00,
            "GOOGL": 150.00,
            "MSFT": 415.20,
            "TSLA": 170.00,
        }
    )


@patch("src.views.card_by_date")
@patch("src.views.transactions_top")
@patch("src.views.exchange_rate")
@patch("src.views.action_price")
@patch("os.path.exists")
@patch("builtins.open")
def test_main_successful(
    mock_open_file,
    mock_exists,
    mock_action_price,
    mock_exchange_rate,
    mock_transactions_top,
    mock_card_by_date,
    mock_cards_df,
    mock_transactions_df,
    fake_settings_json,
):
    """Тест на успешное выполнение функции main"""
    mock_card_by_date.return_value = mock_cards_df
    mock_transactions_top.return_value = mock_transactions_df
    mock_exists.return_value = True
    mock_open_file.return_value.__enter__.return_value.read.return_value = fake_settings_json

    result_main = main("2026-05-15 14:30:00")
    result = json.loads(result_main)

    assert result["greeting"] == "Добрый день"

    assert len(result["cards"]) == 1
    assert result["cards"][0]["last_digits"] == "1234"
    assert result["cards"][0]["total_spent"] == 5500
    assert result["cards"][0]["cashback"] == 55

    assert len(result["top_transactions"]) == 1
    assert result["top_transactions"][0]["date"] == "2026-05-15"
    assert result["top_transactions"][0]["last_digits"] == "1234"
    assert result["top_transactions"][0]["amount"] == 5500
    assert result["top_transactions"][0]["category"] == "Одежда"
    assert result["top_transactions"][0]["description"] == "Покупка пальто"

    assert len(result["currency_rates"]) == 2
    assert result["currency_rates"][0]["currency"] == "USD"
    assert result["currency_rates"][0]["rate"] == 91.50

    assert len(result["stock_prices"]) == 5
    assert result["stock_prices"][0]["stock"] == "AAPL"
    assert result["stock_prices"][0]["price"] == 175.50

    mock_exchange_rate.assert_called_once()
    assert mock_action_price.call_count == 5


@patch("src.views.card_by_date")
@patch("src.views.transactions_top")
@patch("src.views.exchange_rate")
@patch("src.views.action_price")
@patch("os.path.exists")
@patch("builtins.open")
def test_main_date_incorrect(
    mock_open_file,
    mock_exists,
    mock_action_price,
    mock_exchange_rate,
    mock_transactions_top,
    mock_card_by_date,
    mock_cards_df,
    mock_transactions_df,
    fake_settings_json,
):
    """Тест на некорректное введение даты"""
    mock_card_by_date.return_value = mock_cards_df
    mock_transactions_top.return_value = mock_transactions_df
    mock_exists.return_value = True
    mock_open_file.return_value.__enter__.return_value.read.return_value = fake_settings_json

    result_main = main("2026-05-15 14:30")
    result = json.loads(result_main)

    assert result["greeting"] == "Здравствуйте"
    assert "cards" in result


@patch("src.views.card_by_date")
@patch("src.views.transactions_top")
@patch("src.views.exchange_rate")
@patch("src.views.action_price")
@patch("os.path.exists")
@patch("builtins.open")
def test_main_excel_file_empty(
    mock_open_file,
    mock_exists,
    mock_action_price,
    mock_exchange_rate,
    mock_transactions_top,
    mock_card_by_date,
    mock_cards_df,
    mock_transactions_df,
    fake_settings_json,
):
    """Тест на пустой excel-файл"""
    mock_card_by_date.return_value = pd.DataFrame()
    mock_transactions_top.return_value = pd.DataFrame()
    mock_exists.return_value = True
    mock_open_file.return_value.__enter__.return_value.read.return_value = fake_settings_json

    result_main = main("2026-05-15 14:30:00")
    result = json.loads(result_main)

    assert result["cards"] == []
    assert result["top_transactions"] == []


@patch("src.views.card_by_date")
@patch("src.views.transactions_top")
@patch("src.views.exchange_rate")
@patch("src.views.action_price")
@patch("os.path.exists")
@patch("builtins.open")
def test_main_json_file_invalid(
    mock_open_file,
    mock_exists,
    mock_action_price,
    mock_exchange_rate,
    mock_transactions_top,
    mock_card_by_date,
    mock_cards_df,
    mock_transactions_df,
    fake_settings_json,
):
    """Тест на ошибки в json-файле"""
    mock_card_by_date.return_value = mock_cards_df
    mock_transactions_top.return_value = mock_transactions_df
    mock_exists.return_value = True
    mock_open_file.return_value.__enter__.return_value.read.return_value = '{"AMZN": 180.00'

    result_main = main("2026-05-15 14:30:00")
    result = json.loads(result_main)

    assert result["currency_rates"] == []
    assert result["stock_prices"] == []
