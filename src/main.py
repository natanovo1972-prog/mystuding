import json
import os
from datetime import datetime

import pandas as pd

from src.reports import spending_by_weekday
from src.services import transactions_by_phone
from src.views import main


def application():
    """Функция запускает приложние для анализа транзакций из excel-файла, а также
    получения курса валют и стоимости акций S&P500 на основе полученной даты"""
    print("Привет!\nДобро пожаловать в приложение")
    print("Введите дату в формате ДД-ММ-ГГГГ или ДД.ММ.ГГГГ (например, 25-03-2025 или 25.03.2025):")
    user_input = input().strip()
    user_input = user_input.replace(".", "-")
    try:
        user_date = datetime.strptime(user_input, "%d-%m-%Y")
        date_final = user_date.strftime("%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты. Попробуйте снова.")

    # Загружаем путь до файла с транзакциями
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "operations.xlsx")

    # Получаем JSON-строку из функции main
    json_data = main(date_final)
    # Превращаем JSON-строку в словарь PYthon
    data_for_user = json.loads(json_data)

    # Выводим приветствие
    print(f"\n{data_for_user['greeting']}\n")

    while True:
        print("\n---Главное меню---")
        print("1. Общая сумма расходов и кэшбэк по номеру карты")
        print("2. Топ-5 транзакций по сумме платежа")
        print("3. Курс валют")
        print("4. Стоимость акций S&P500")
        print("5. Средние траты за каждый день недели за последние три месяца от указанной даты")
        print("6. Выбор транзакций по телефонным номерам")
        print("0. Выход из приложения")

        user_choice = input("\nВыберите пункт меню (0-6): ").strip()

        if user_choice == "1":
            print("\n---1. Общая сумма расходов и кэшбэк по номеру карты.---")
            cards = data_for_user.get("cards", [])
            if cards:
                for card in cards:
                    print(
                        f"Карта *{card['last_digits']}: "
                        f"Расходы *{card['total_spent']:.2f} руб.,"
                        f"Кэшбэк *{card['cashback']} руб."
                    )
            else:
                print("Данные по картам не найдены.")

        elif user_choice == "2":
            print("\n---2. Топ-5 транзакций по сумме платежа.---")
            transactions = data_for_user.get("top_transactions", [])
            if transactions:
                number = 1
                for tr in transactions:
                    print(
                        f"{number}. {tr['date']} | Карта *{tr['last_digits']} | "
                        f"{tr['amount']:.2f} руб. | {tr['category']} | {tr['description']}"
                    )
                    number = number + 1
            else:
                print("Данные по транзакциям не найдены")

        elif user_choice == "3":
            print("\n---3. Курс валют.---")
            currencies = data_for_user.get("currency_rates", [])
            if currencies:
                for currency in currencies:
                    print(f"{currency['currency']}: {currency['rate']:.2f} руб.")
            else:
                print("Данные по курсу валют не доступны.")

        elif user_choice == "4":
            print("\n---4. Стоимость акций S&P500.---")
            stocks = data_for_user.get("stock_prices", [])
            if stocks:
                for stock in stocks:
                    print(f"stock{'stock'}: ${stock['price']:.2f}")
            else:
                print("Данные по стоимости акций не доступны")

        elif user_choice == "5":
            print("\n---5. Средние траты за каждый день недели за последние три месяца" "\nот указанной даты.---")
            try:
                # Читаем данные из excel-файла
                all_transactions = pd.read_excel(DATA_PATH)
                # Вызываем функцию
                spending_by_weekday(all_transactions, date_final)
                files = [f for f in os.listdir(".") if f.startswith("report_") and f.endswith(".csv")]
                if files:
                    latest_file = max(files, key=os.path.getmtime)
                    df_report = pd.read_csv(latest_file, sep=";", encoding="utf-8-sig")
                    if not df_report.empty:
                        day_column = df_report.columns[0]
                        spend_column = df_report.columns[1]
                        for _, row in df_report.iterrows():
                            print(f"{row[day_column]}: {float(row[spend_column]):.2f} руб.")
                    else:
                        print("Файл отчета пуст")
                else:
                    print("Нет данных за указанный период")

            except Exception as e:
                print(f"Не удалось рассчитать траты за указанный период: {e}")

        elif user_choice == "6":
            print("\n---6. Выбор транзакций по телефонным номерам.___")
            phone_json = transactions_by_phone(DATA_PATH)
            phone_transactions = json.loads(phone_json)
            if phone_transactions:
                number = 1
                for tr in phone_transactions:
                    print(
                        f"{number}. {tr.get('Дата операции', '')} | "
                        f"{tr.get('Сумма операции', 0):.2f} руб. | {tr.get('Описание', '')}"
                    )
                    number = number + 1
            else:
                print("Транзакции с телефонными номерами не найдены.")

        elif user_choice == "0":
            print("\nСпасибо за использование приложения.")
            break
        else:
            print("\nОшибка. Неверный ввод. Введите цифру от 0 до 6.")


if __name__ == "__main__":
    application()
