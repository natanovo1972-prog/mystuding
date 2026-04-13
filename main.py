from src.generators import filter_by_currency
from src.process_bank import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.transactions_reader import transactions_csv, transactions_excel
from src.utils import fin_transaction
from src.widget import get_date, mask_account_card


def main():
    """Функция определяет основную логику проекта и связывает функциональности между собой"""
    while True:
        print("Привет!\nДобро пожаловать в программу работы с банковскими транзакциями.")
        print(
            "Выберите необходимый пункт меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла.\n"
            "2. Получить информацию о транзакциях из CSV-файла.\n"
            "3. Получить информацию о транзакциях из XLSX-файла.")
        user_choice = (input("Вы выбрали: ").strip())
        if user_choice == "1":
            print("Для обработки выбран JSON-файл.")
            file_path = "data/operations.json"
            transactions = fin_transaction(file_path)
            break
        elif user_choice == "2":
            print("Для обработки выбран CSV-файл.")
            file_path = "data/transactions.csv"
            transactions = transactions_csv(file_path)
            break
        elif user_choice == "3":
            print("Для обработки выбран XLSX-файл.")
            file_path = "data/transactions_excel.xlsx"
            transactions = transactions_excel(file_path)
            break
        else:
            print("Выбор неверный. Выберите 1, 2 или 3.")
            continue

    while True:
        print("Введите статус, по которому выполнить фильтрацию.\n"
              "Доступные статусы: EXECUTED, CANCELED, PENDING.")
        status = ["EXECUTED", "CANCELED", "PENDING"]
        user_status = (input().strip().upper())
        if user_status in status:
            filter_status = user_status
            print(f"Выбран статус: {filter_status}")
            sort_state = filter_by_state(transactions, filter_status)
            break
        else:
            print("Операции по данному статусу недоступны.\n"
                  "Введите статус, по которому необходимо выполнмть фильтрацию.\n"
                  "Доступные статусы: EXECUTED, CANCELED, PENDING.")

    sort_by_data_choice = ""
    while sort_by_data_choice not in ["да", "нет"]:
        sort_by_data_choice = input("Отсортировать выбранные операции по дате? Да/Нет.").strip().lower()
        if sort_by_data_choice == "да":
            sort_by_order = input("Отсортировать по возрастанию или убыванию?").strip().lower()
            if "возраст" in sort_by_order:
                filter_order = sort_by_date(sort_state, False)
            elif "убыван" in sort_by_order:
                filter_order = sort_by_date(sort_state, True)
            else:
                filter_order = sort_state
            break
        elif sort_by_data_choice == "нет":
            filter_order = sort_state
            break

    sort_by_transaction_choice = ""
    while sort_by_transaction_choice not in ["да", "нет"]:
        sort_by_transaction_choice = input("Выводить только рублевые транзакции? Да/Нет.").strip().lower()
        if sort_by_transaction_choice == "да":
            sort_transaction = "RUB"
            transactions_rub = list(filter_by_currency(filter_order, sort_transaction))
            break
        elif sort_by_transaction_choice == "нет":
            transactions_rub = filter_order
            break

    sort_by_word = (input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет.").
                    strip().lower())
    if sort_by_word == "да":
        filter_word = input("Введите слово для транзакций по описанию.").strip()
        filter_transactions = process_bank_search(transactions_rub, filter_word)
    else:
        filter_transactions = transactions_rub

    print("Распечатываю итоговый список транзакций")
    if not filter_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    print(f"\nВсего банковских операций в списке: {len(filter_transactions)}\n")
    for transaction in filter_transactions:
        raw_date = transaction.get("date", "")
        date = get_date(raw_date) if raw_date else "00.00.0000"
        description = transaction.get("description", "Перевод")
        from_info = transaction.get("from", "")
        to_info = transaction.get("to", "")
        from_account = mask_account_card(from_info)
        to_account = mask_account_card(to_info)

        if user_choice == "1":
            amount = transaction.get("operationAmount", {}).get("amount", "0")
            currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", "")
        else:
            amount = transaction.get("amount", "0")
            currency = transaction.get("currency_code", "руб.")

        print(f"{date} {description}")
        if from_account:
            print(f"{from_account} -> {to_account}")
        else:
            print(f"{to_account}")

        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
