import re
import os
import requests
import openpyxl
import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

start_time = time.time()


def setup_driver():
    user_agent = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")
    options.add_argument("--headless")  # Запускает Chrome без графического интерфейса
    options.add_argument("--disable-gpu")  # Отключает GPU Chrome
    options.add_argument("--no-sandbox")  # Запускает Chrome в отсутствии безопасности sandbox
    options.add_argument("--disable-dev-shm-usage")  # Использует систему разделения памяти
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    return webdriver.Chrome(options=options)


def get_num_page(driver):
    url = "https://www.zappos.com/filters/shoes-shoes/CK_XAeICAQE.zso?t=shoes&p="
    driver.get(url)

    last_page_num = int(driver.find_element(By.XPATH, '//*[@id="searchPagination"]/div[2]/span/a[4]').text)

    print(last_page_num)
    if last_page_num < 390:
        driver.close()
        return main()
    return last_page_num


def get_pages(driver, last_page_num):
    url = "https://www.zappos.com/filters/shoes-shoes/CK_XAeICAQE.zso?t=shoes&p="
    urls = []

    for page_number in range(0, last_page_num - 1):
        time.sleep(random.uniform(1, 3))
        current_url = f'{url}{page_number}'
        driver.get(current_url)
        print(driver.title)
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")
        base_section = soup.find_all("a")

        for item in base_section:
            base_section_url = item.get("href")
            urls.append(base_section_url)

        # Remove duplicates
        urls = list(set(urls))

        with open('zappos_shoes_urls.txt', 'w') as file:
            for full_url in urls:
                if full_url is not None and "/p/" in full_url:
                    file.write(f"https://www.zappos.com{full_url}\n")
                else:
                    continue


def main():
    with setup_driver() as driver:
        try:
            last_page_num = get_num_page(driver)
            get_pages(driver, last_page_num)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

end_time = time.time()
total_time = round(end_time - start_time, 1)
print(f"Программа завершена за {total_time} секунд.")  # Выводим общее время выполнения программы
