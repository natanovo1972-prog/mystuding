from unittest.mock import mock_open, patch

import pandas as pd

from src.transactions_reader import transactions_csv, transactions_excel


def test_transactions_csv_success():
    """Тестируем успешное чтение csv-файла """
    mock_get = "id;amount;currency\n2;200;RUB\n3;300;USD"  # Имитируем содержимое csv-файла
    with patch("builtins.open", mock_open(read_data=mock_get)):
        result = transactions_csv("test_path_csv")

        assert result == [
            {"id": "2", "amount": "200", "currency": "RUB"},
            {"id": "3", "amount": "300", "currency": "USD"}
        ]


def test_transactions_csv_error():
    """Тестируем, что csv-файл не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = transactions_csv("empty_path_csv")

        assert result == []


@patch("pandas.read_excel")
def test_transactions_excel_success(mock_read_excel):
    """Тестируем успешное чтение excel-файла"""
    df = pd.DataFrame([
                      {"id": 2, "amount": 200, "currency": "RUB"},
                      {"id": 3, "amount": 300, "currency": "USD"}
                      ])
    mock_read_excel.return_value = df
    expected = df.to_dict(orient="records")
    result = transactions_excel("test_path_excel")
    assert result == expected


@patch("pandas.read_excel")
def test_transactions_excel_error(mock_read_excel):
    """Тестируем ошибку отсутствия файла"""
    mock_read_excel.side_effect = FileNotFoundError
    result = transactions_excel("fake_path_excel")
    expected = []
    assert result == expected
