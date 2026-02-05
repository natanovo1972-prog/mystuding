from functools import wraps
import time
from black.lines import Callable


def log(filename=None) -> Callable:
    def log_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start_f = time.time()
            result = None
            error_msg = ""
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                # Вводим информацию об ошибке
                error_msg = (f"{function.__name__} raised with arguments {args, kwargs} but it didn't worked,"
                             f"error:{str(e)} \n")
            finally:
                finish_f = time.time()
                raise_time = finish_f - start_f
                # Вводим итоговое сообщение: ошибка (если нужно) и время выполнения функции
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
    def my_function(x, y):
        return x + y

    my_function(1, 2)
