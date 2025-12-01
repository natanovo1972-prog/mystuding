import re

def clear_names(file_name: str) -> list:
    """Функция по очистке списка имен от лишних символов"""
    new_names_list = list()
    with open('data/' + file_name) as names_file:
        names_list = names_file.read().split()
        for name_item in names_list:
            new_name = ''
            for symbol in name_item:
                if symbol.isalpha():
                    new_name += symbol
            if new_name.isalpha():
                new_names_list.append(new_name)
    return new_names_list


def is_cyrillic(name_item: str) -> bool:
    """Функция фильтрует перечень имен на наличие имен на кириллице"""
    return bool(re.search(r'[а-яА-Я]', name_item))


def filter_russian_names(names_list: list) -> list:
    """Функция принимает на вход список имен и выводит только русские имена"""
    new_name_list = list()
    for name_item in names_list:
        if is_cyrillic(name_item):
            new_name_list.append(name_item)
    return new_name_list


if __name__ == '__main__':
    cleared_names = clear_names('names.txt')

    print(filter_russian_names(cleared_names))


