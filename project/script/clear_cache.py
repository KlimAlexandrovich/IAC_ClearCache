from selenium.webdriver.common.by import By
from selenium import webdriver
import logging
from typing import Any


class Cleaner:
    def __init__(self):
        self.driver = webdriver.Edge()
        self.auth_url = "http://10.24.131.126"
        self.cache_url = f"{self.auth_url}/os/org-structure"
        self.user_name = "АдминистраторИС"
        self.user_password = "АдминистраторИС"

    @staticmethod
    def _login(driver: Any, name: str, password: str):
        try:
            username_input = driver.find_element(By.NAME, "name")
            password_input = driver.find_element(By.NAME, "pass")
            submit_button = driver.find_element(By.ID, "edit-submit")
            # Вводим ваши учетные данные
            username_input.send_keys(name)
            password_input.send_keys(password)
            # Отправляем форму
            submit_button.click()
            return True
        except Exception as error:
            return False

    @staticmethod
    def _clear_cache(driver: Any):
        try:
            reset_caches_button = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/ul/li[2]/a')
            reset_caches_button.click()
            reset_button = driver.find_element(By.ID, "edit-submit")
            reset_button.click()
        except Exception as error:
            return False

    def clear_cache(self):
        try:
            # Создание сессии.
            driver = webdriver.Edge()
            # Авторизация.
            driver.get(self.auth_url)
            self._login(driver=driver, name=self.user_name, password=self.user_password)
            # Очистка кэша.
            driver.get(self.cache_url)
            self._clear_cache(driver=driver)
            # Закрытие окна сессии.
            driver.quit()
            return True
        except Exception as error:
            # text = f"Error at {Cleaner.login}.\nError message: {error}"
            return False


if __name__ == "__main__":
    try:
        clean_service = Cleaner()
        clean_service.clear_cache()
    except Exception as error:
        text = f"{error=}"
