from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import random

if __name__ == "__main__":
    try:
        service, options = webdriver.ChromeService(), webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(f'https://www.example.com')
        time.sleep(20)
        driver.quit()
        print("Done!")
    except Exception as e:
        print(f"{e=}")
