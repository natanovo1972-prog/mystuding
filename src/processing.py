from typing import List, Dict


def filter_by_state(list_dictionary: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Функция принимает на вход список словарей с данными о банковских операциях и параметр state,
    и возвращает новый список, содержащий только те словари, у которых ключ state содержит переданное
    в функцию значение"""
    new_list_dictionary = []
    for item in list_dictionary:
        if item.get("state") == state:
            new_list_dictionary.append(item)
    return new_list_dictionary


def sort_by_date(list_dictionary_date: List[Dict], date: bool = True) -> List[Dict]:
    """Функция принимает на вход список словарей и параметр порядка сортировки, и возвращает новый список,
    в котором исходные словари отсортированы по дате"""
    new_list_by_date = sorted(list_dictionary_date, key=lambda data: data["date"], reverse=date)
    return new_list_by_date


if __name__ == "__main__":
    test = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(filter_by_state(test))

    test_date = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(sort_by_date(test_date))
