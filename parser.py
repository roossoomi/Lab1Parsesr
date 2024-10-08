from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import os
import logging

# Настройка логирования
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

driver = webdriver.Firefox()
driver.get("https://1000.menu/catalog/tortj")

# Проверка корректности подгружаемого сайта
title_name = "Торт"
try:
    assert title_name in driver.title
    logging.info("Сайт загружен успешно.")
except AssertionError:
    logging.error("Ошибка загрузки сайта. Заголовок не соответствует ожидаемому.")


with open('linksss.txt', 'w') as f:
    collected_links = set()
    while True:
        links = driver.find_elements(By.XPATH, "//a[contains(@class, 'h5')]")
        for link in links:
            href = link.get_attribute("href")
            if href not in collected_links:
                collected_links.add(href)
                f.write(href + "\n")

        try:
            next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'cb') and contains(@class, 'red')]")
            next_button.click()
            time.sleep(4)
            logging.info("Клик на кнопку 'Далее'.")
        except (NoSuchElementException, ElementClickInterceptedException):
            logging.info("Кнопка 'Далее' не найдена. Завершение сбора ссылок.")
            break
driver.quit()


os.makedirs('htmlll_files', exist_ok=True)
with open('linksss.txt', 'r') as f:
    for index, link in enumerate(f, start=1):
        try:
            response = requests.get(link)
            with open(f'htmlll_files/page_{index}.html', 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)
                print(index)
        except requests.RequestException:
            logging.error(f"Ошибка при загрузке страницы: {link}")


print("Загрузка завершена.")
