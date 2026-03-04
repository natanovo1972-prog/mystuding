from unittest.mock import patch

from src.external_api import summa_transactions


def test_summa_transaction_ruble_correct():
    """Тестируем корректное получение транзакции в рублях"""
    transaction = {"currency": "RUB", "amount": 300}
    assert summa_transactions(transaction) == 300


@patch("requests.request")
def test_summa_transaction_not_ruble_correct(mock_get):
    """Тестируем корректный перевод транзакции в рубли"""
    mock_reply = mock_get.return_value
    mock_reply.status_code = 200
    mock_reply.json.return_value = {"result": 45000.0}

    transaction = {"amount": 500, "currency": "USD"}
    result = summa_transactions(transaction)
    assert result == 45000.0

    mock_get.assert_called_with(
        "GET", "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=500.0",
        headers={"apikey": "9J3Z5hXxUwVOI5gGke3jpRV5vDZmJ0OM"}, data={})


@patch("requests.request")
def test_summa_transaction_server_error(mock_get):
    """Ошибка запроса к серверу"""
    mock_get.return_value.status_code = 500
    transaction = {"amount": 200, "currency": "EUR"}
    result = summa_transactions(transaction)
    assert result == 0.0


@patch("requests.request")
def test_summa_transaction_exception(mock_get):
    """Тест на исключение"""
    mock_get.side_effect = Exception("Connection Error")
    transaction = {"amount": 200, "currency": "EUR"}
    result = summa_transactions(transaction)
    assert result == 0.0
