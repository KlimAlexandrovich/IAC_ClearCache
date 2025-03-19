from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import datetime
import logging
from typing import Any
from project.config import LOGS_FILE_PATH, DEFAULT_LOGS_FILE, DRIVER_TIMEOUT
from project.utils.decorators import driver_exception_handler


class Cleaner:
    def __init__(self, path_to_logs_file: str, driver: Any):
        self.driver = driver
        self.auth_url = "http://10.24.131.126"
        self.cache_url = f"{self.auth_url}/os/org-structure"
        # Данные для авторизации.
        self.user_name = "АдминистраторИС"
        self.user_password = "АдминистраторИС"
        # Определяем настройки для логирования событий.
        self.logs_file = path_to_logs_file
        self.logs_format = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(level=logging.INFO, filename=self.logs_file, format=self.logs_format)
        logging.basicConfig(level=logging.WARNING, filename=self.logs_file, format=self.logs_format)

    @staticmethod
    @driver_exception_handler
    def _login(driver: Any, name: str, password: str) -> bool:
        """
        Вспомогательная функция для авторизации в информационной системе.

        Parameters
        ----------
        driver : selenium.webdriver
            Веб-драйвер для работы с браузером.
        name : str
            Логин для авторизации.
        password : str
            Пароль для авторизации.

        Returns
        -------
        bool
            Статус выполнения команд.
        """
        # Находим форму.
        username_input = driver.find_element(By.NAME, "name")
        password_input = driver.find_element(By.NAME, "pass")
        submit_button = driver.find_element(By.ID, "edit-submit")
        # Вводим учетные данные.
        username_input.send_keys(name)
        password_input.send_keys(password)
        # Отправляем форму.
        submit_button.click()

    @staticmethod
    @driver_exception_handler
    def _clear_cache(driver: Any) -> bool:
        """
        Вспомогательная функция для очистки кэша.

        Parameters
        ----------
        driver : selenium.webdriver
            Веб-драйвер для работы с браузером.
        Returns
        -------
        bool
            Статус выполнения команд.
        """
        reset_caches_button = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/ul/li[2]/a')
        reset_caches_button.click()
        reset_button = driver.find_element(By.ID, "edit-submit")
        reset_button.click()

    @driver_exception_handler
    def clear_cache(self) -> bool:
        # Авторизация.
        self.driver.get(self.auth_url)
        self._login(driver=self.driver, name=self.user_name, password=self.user_password)
        # Очистка кэша.
        self.driver.get(self.cache_url)
        self._clear_cache(driver=self.driver)


if __name__ == "__main__":
    # Определяем файл для логирования состояний сервера.
    logs_file = LOGS_FILE_PATH if os.path.exists(LOGS_FILE_PATH) else DEFAULT_LOGS_FILE
    # Инициализируем веб-драйвер и его параметры.
    service, options = webdriver.ChromeService(), webdriver.ChromeOptions()
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(DRIVER_TIMEOUT)  # Установка таймаута загрузки страницы.# Установка неявного ожидания.
    browser.implicitly_wait(DRIVER_TIMEOUT)  # Установка неявного ожидания.
    # Запускаем скрипт.
    clean_service = Cleaner(path_to_logs_file=logs_file, driver=browser)
    response = clean_service.clear_cache()
    # По завершению работы скрипта ОБЯЗАТЕЛЬНО закрываем драйвер и открывшиеся окно браузера.
    browser.quit()
    # В зависимости от результата работы скрипта, логируем результат работы.
    if response:
        logging.info(f"{datetime.datetime.now()} -- Cache cleared successfully.")
        response = "1"
    else:
        response = "0"
    print(response)  # Для обработки ответа скрипта со стороны севера Flask.
