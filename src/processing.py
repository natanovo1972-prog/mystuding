from typing import List, Dict, Any

def filter_by_state(list_dictionary: List[Dict[str, Any]], state = 'EXECUTED') -> List[Dict[str, Any]]:
    ##Функция принимает список словарей и значение ключа, и возвращает новый список словарей, у которых ключ соответствует указанному значению##
    new_list_dictionary = []
    for d in list_dictionary:
        if d.get('state') == state:
            new_list_dictionary.append(d)
    return new_list_dictionary


def sort_by_date(list_dictionary_date: List[Dict[str, Any]], date: bool=True) -> List[Dict[str, Any]]:
    ##Функция принимает список словарей и параметр сортировки по убыванию, и возвращает новый список, отсортированный по дате##
    new_list_by_date = sorted(list_dictionary_date, key=lambda data: data["date"], reverse=date)
    return new_list_by_date


if __name__=="__main__":
    test = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    print(filter_by_state(test))

    test_date = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    print(sort_by_date(test_date))


