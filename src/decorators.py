from functools import wraps
import time
from typing import Callable, Any


def log(filename=None) -> Callable:
    """Декоратор для логирования работы функции
    Args: filename - пусть к файлу лога, None - вывод в консоль
    Returns: декоратор принимает функцию и возвращает обертку"""
    def log_decorator(function: Callable) -> Callable:
        """Декоратор логирует начало и конец функции, ее результаты и ошибки"""
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка, замеряющая время выполнения и обрабатывающая исключения"""
            start_f = time.time()
            result = None
            error_msg = ""
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                # Информация об ошибке
                error_msg = (f"{function.__name__} raised with arguments {args, kwargs} but it didn't worked,"
                             f"error:{str(e)} \n")
            finally:
                finish_f = time.time()
                raise_time = finish_f - start_f
                # Итоговое сообщение: ошибка (если нужно) и время выполнения функции
                status = "finished" if not error_msg else "finished with error"
                msg = f"{error_msg}{raise_time}s {function.__name__} {status}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(msg + "\n")
                else:
                    print(msg)
            return result

        return wrapper
    return log_decorator


if __name__ == "__main__":

    @log(filename="my_file.txt")
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, 2)
