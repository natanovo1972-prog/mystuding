import json
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import action_price, card_by_date, exchange_rate, transactions_top


@pytest.fixture
def common_data():
    """Создаем фикстуру с общими данными для тестов"""
    return pd.DataFrame(
        {
            "Дата платежа": ["01.02.2025", "02.02.2025", "03.02.2025"],
            "Номер карты": ["*1234", "*1234", None],
            "Сумма операции": [300.00, 500.00, 1000.0],
            "Категория": ["Транспорт", "Досуг", "Супермаркеты"],
            "Описание": ["Покупка_1", "Покупка_2", "Покупка_3"],
            "Кэшбэк": [3, 5, 10],
        }
    )


def test_card_by_date_successful(common_data):
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = common_data
        # Вызываем функцию
        result = card_by_date("test.xlsx")
        card = result[result["Последние 4 цифры номера карты"] == "1234"].iloc[0]
        assert card["Сумма операции"] == 800.00
        assert card["Кэшбэк"] == 8


@patch("pandas.read_excel")
def test_card_by_date_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")
    result = card_by_date("file_not_exist.xlsx")
    assert result.empty


@patch("pandas.read_excel")
def test_transactions_top_successful(mock_read_excel, common_data):
    mock_read_excel.return_value = common_data
    result = transactions_top("test.xlsx")
    # Проверяем, что сумма 1000.00 должна стоять первой строкой
    assert result.iloc[0]["Сумма операции"] == 1000.00
    # Проверяем обработку None
    assert result.iloc[0]["Последние 4 цифры номера карты"] == "Не указана"


@patch("pandas.read_excel")
def test_transaction_top_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")
    result = transactions_top("file_not_exist.xlsx")
    assert result.empty


@patch("requests.get")
@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='{"AAPL": 150.0}')
def test_exchange_rate_successful(mock_file, mock_exists, mock_get):
    mock_exists.return_value = True  # Имитируем, что файл существует
    # Имитируем ответ API
    mock_get.return_value.json.return_value = {"status": 200, "data": {"USDRUB": "85.00", "EURRUB": "100.00"}}
    # Запускаем функцию
    exchange_rate()
    opened_file = mock_file()
    written_data = "".join(call.args[0] for call in opened_file.write.call_args_list)
    if not written_data:
        written_data = "".join(call.args[0] for call in mock_file.return_value.write.call_args_list)
    result = json.loads(written_data)
    assert result["AAPL"] == 150.0
    assert result["USDRUB"] == "85.00"
    assert result["EURRUB"] == "100.00"


@patch("requests.get")
@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='{"AAPL": 150.0}')
def test_exchange_rate_api_empty_response(mock_file, mock_exists, mock_get):
    mock_exists.return_value = True
    mock_get.return_value.json.return_value = {"status": 403, "message": {"Invalid API-key"}, "data": {}}
    exchange_rate()
    mock_file().write.assert_not_called()


@patch("yfinance.Ticker")
@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='{"USDRUB": "90.0"}')
def test_action_price_successful(mock_file, mock_exists, mock_ticker):
    mock_exists.return_value = True
    mock_data = pd.DataFrame({"Close": [200.0]})
    mock_ticker.return_value.history.return_value = mock_data
    action_price("TSLA")
    written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)
    result = json.loads(written_data)
    assert result["USDRUB"] == "90.0"
    assert result["TSLA"] == 200.0


@patch("yfinance.Ticker")
@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='{"USDRUB": "90.0"}')
def test_action_price_not_found(mock_file, mock_exists, mock_ticker):
    mock_exists.return_value = True
    mock_ticker.return_value.history.return_value = pd.DataFrame
    action_price("unknown_ticker")
    mock_file().write.assert_not_called()
