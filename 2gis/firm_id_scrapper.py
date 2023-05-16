from telnetlib import EC
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from selenium.webdriver.chrome.options import Options


def search_salons(query, driver):
    search_box = driver.find_element("xpath", "//input[@class='_1gvu1zk' and @placeholder='Search in 2GIS']")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Allow the search results to load


def create_transitional_df(path, driver):
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=["name", "category", "address", "link"])

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "_awwm2v")]')))
    except TimeoutException:
        print("Timeout waiting for search results")

    time.sleep(2)
    results = driver.find_elements("xpath", '//div[contains(@class, "_awwm2v")]/div/div[contains(@class, "_1kf6gff")]')

    for result in results:
        try:
            entry = {
                "name": 'Not Available',
                "category": 'Not Available',
                "address": 'Not Available',
                "link": 'Not Available',
            }
            name_element = result.find_element("xpath",
                                               './/div[contains(@class, "_zjunba")]//a[contains(@class, ''"_1rehek")]')

            name = name_element.get_attribute("textContent").strip()
            entry['name'] = name

            category_element = result.find_element("xpath", './/span[contains(@class, "_oqoid")]')
            category = category_element.get_attribute("textContent").strip()
            entry['category'] = category

            address_element = result.find_element("xpath", './/span[contains(@class, "_1w9o2igt")]')
            address = address_element.get_attribute("textContent").strip()
            entry['address'] = address

            link_element = result.find_element("xpath",
                                               './/div[contains(@class, "_zjunba")]//a[contains(@class, "_1rehek")]')
            link = link_element.get_attribute("href")
            entry['link'] = link

            df = df._append(entry, ignore_index=True)
            df.to_csv(path, index=False)

        except NoSuchElementException:
            continue


def main():

    URL = "https://2gis.ae/"
    query = 'barber shop in ajman'
    transitional_df_path = "../resources/transitional_df.csv"
    firm_id_scrapper_path = "../out/firm_id_scrapper_log.txt"

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(URL)
    search_salons(query, driver)

    while True:

        create_transitional_df(transitional_df_path, driver)
        wait = WebDriverWait(driver, 100)
        buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._n5hmn94')))

        element = buttons[0]
        if len(buttons) >= 2:
            element = buttons[1]
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)

        with open(firm_id_scrapper_path, "a") as file:
            file.write(f"{driver.current_url}\n")


if __name__ == "__main__":
    main()
