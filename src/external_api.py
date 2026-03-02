import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def summa_transactions(transaction) -> float:
    """Функция принимает транзакцию и возвращает сумму транзакций в рублях в виде числе с точкой"""
    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency")

    if currency == "RUB":
        return amount
    if currency == "USD" or currency == "EUR":
        url = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}".format(
              "RUB", currency, amount)
        payload = {}
        headers = {"apikey": API_KEY}
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                return float(data.get("result", 0))
            else:
                print(f"Ошибка сервера: {response.status_code}, Текст: {response.text}")
                return 0.0
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return 0.0


if __name__ == "__main__":  # pragma: no cover
    test_1 = {"amount": 500, "currency": "USD"}
    test_2 = {"amount": 3500, "currency": "RUB"}
    result_1 = summa_transactions(test_1)
    result_2 = summa_transactions(test_2)
    print(result_1)
    print(result_2)
