import json
import os.path
from datetime import datetime, time

from src.utils import action_price, card_by_date, exchange_rate, get_setting_path, transactions_top


def create_greeting(date_str: str) -> str:
    """Функция формирует приветствие на основе времени, указанном в дате"""
    current_hour = datetime.now().time()
    if time(6, 0) <= current_hour <= time(11, 59, 59):
        return "Доброе утро"
    elif time(12, 0) <= current_hour <= time(17, 59, 59):
        return "Добрый день"
    elif time(18, 0) <= current_hour <= time(22, 59, 59):
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def main(date_str: str):
    """Функция принимает строку с датой и возвращает JSON-ответ со следующими данными:
    приветствие, по каждой карте: последние 4 цифры номера, расходы, кэщбкэ; топ-5 транзакций
    по сумме платежа, курс валют, стоимость акций s&p500"""
    greeting = create_greeting(date_str)
    df_cards = card_by_date()
    cards = []
    if not df_cards.empty:
        for _, row in df_cards.iterrows():
            cards.append(
                {
                    "last_digits": str(row["Последние 4 цифры номера карты"]),
                    "total_spent": float(row["Сумма операции"]),
                    "cashback": int(row["Кэшбэк"]),
                }
            )
    df_transactions = transactions_top()
    transactions = []
    if not df_transactions.empty:
        for _, row in df_transactions.iterrows():
            transactions.append(
                {
                    "date": str(row["Дата платежа"]),
                    "last_digits": str(row["Последние 4 цифры номера карты"]),
                    "amount": float(row["Сумма операции"]),
                    "category": str(row["Категория"]),
                    "description": str(row["Описание"]),
                }
            )
    # Записываем данные курса валют и акций в user_settings.json
    exchange_rate()
    for ticker in ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]:
        action_price(ticker)
    # Читаем данные из user_settings.json
    settings_path = get_setting_path()
    currencies = []
    stocks = []
    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for currency in ["USD", "EUR"]:
                    pair = f"{currency}RUB"
                    if pair in data:
                        currencies.append({"currency": currency, "rate": float(data[pair])})
                for ticker in ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]:
                    if ticker in data:
                        stocks.append({"stock": ticker, "price": float(data[ticker])})
            except json.JSONDecodeError:
                print("Ошибка чтения файла user_settings.json")
    # Формируем финальный JSON
    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": transactions,
        "currency_rates": currencies,
        "stock_prices": stocks,
    }
    return json.dumps(response, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    result = main("2026-05-15 14:30:00")
    print(result)
