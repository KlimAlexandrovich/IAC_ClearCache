import logging
from typing import Callable


def driver_exception_handler(func: Callable) -> Callable:
    """ Декоратор для команд веб-драйвера selenium.webdriver.
        Оборачивает функцию и возвращает True, если в процессе работы не возникло исключений.
        Иначе возвращает False. """

    def wrapper(*args, **kwargs) -> bool:
        try:
            _ = func(*args, **kwargs)
            return True
        except Exception as error:
            logging.warning(f"{func} was failed. Exception description:\n{error}")
            return False

    return wrapper
