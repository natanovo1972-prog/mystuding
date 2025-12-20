def filter_by_state(list_dictionary: [{}], state = 'EXECUTED') -> []:
    ##Функция принимает список словарей и значение ключа, и возвращает новый список словарей, у которых ключ соответствует указанному значению##
    new_list_dictionary = []
    for d in list_dictionary:
        if d.get('state') == state:
            new_list_dictionary.append(d)
    return new_list_dictionary


if __name__=="__main__":
    test = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    print(filter_by_state(test))

