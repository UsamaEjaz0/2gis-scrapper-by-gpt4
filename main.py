from telnetlib import EC
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from selenium.webdriver.chrome.options import Options

num = 1
skipped = 0
firm_info_list = []


def search_salons(query, driver):
    search_box = driver.find_element("xpath", "//input[@class='_1gvu1zk' and @placeholder='Search in 2GIS']")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Allow the search results to load


def store_csv(filename):
    global firm_info_list
    global num
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(
            columns=["Name", "Given Name", "Additional Name", "Family Name", "Yomi Name", "Given Name Yomi",
                     "Additional Name Yomi", "Family Name Yomi", "Name Prefix", "Name Suffix", "Initials",
                     "Nickname", "Short Name", "Maiden Name", "Birthday", "Gender", "Location",
                     "Billing Information", "Directory Server", "Mileage", "Occupation", "Hobby",
                     "Sensitivity", "Priority", "Subject", "Notes", "Language", "Photo", "Group Membership",
                     "E-mail 1 - Type", "E-mail 1 - Value", "Phone 1 - Type", "Phone 1 - Value",
                     "Phone 2 - Type", "Phone 2 - Value", "Organization 1 - Type", "Organization 1 - Name",
                     "Organization 1 - Yomi Name", "Organization 1 - Title", "Organization 1 - Department",
                     "Organization 1 - Symbol", "Organization 1 - Location", "Organization 1 - Job Description"])

    for firm_info in firm_info_list:

        if df['Phone 1 - Value'].isin([int(firm_info['phone'])]).any():
            print(firm_info['phone'])
            print(f"Duplicate: {firm_info['name']} ")

        else:
            row = {
                "Name": "GS " + str(num) + " " + firm_info['name'],
                "Given Name": "GS " + str(num) + " " + firm_info['name'],
                "Phone 1 - Type": "Mobile",
                "Phone 1 - Value": firm_info['phone'],
                "Organization 1 - Name": firm_info['category']
            }

            df = df._append(row, ignore_index=True)
            print(f"Added GS {num} {firm_info['name']}")
            num += 1

    df.to_csv(filename, index=False)


def extract_business_info(driver, data):
    global firm_info_list, skipped
    for single_card in data:
        driver.get(single_card['link'])
        time.sleep(3)
        try:
            firm_info = {
                "name": single_card['name'],
                "category": single_card['category'],
                "address": single_card['address'],
            }

            # Phone number
            try:
                phone_element = driver.find_element("xpath", '//a[contains(@href, "tel:")]')
                phone_number = phone_element.get_attribute('href').split(':')[1].strip()
                firm_info['phone'] = phone_number
            except Exception as e:
                print(f"Skipped {skipped} ")
                skipped += 1
                continue

            firm_info_list.append(firm_info)
        except NoSuchElementException as e:
            print(f"Error in: {single_card['name']}")


def parse_results(driver):
    global firm_info_list
    try:
        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "_awwm2v")]')))
    except TimeoutException:
        print("Timeout waiting for search results")
        return []
    time.sleep(3)
    results = driver.find_elements("xpath", '//div[contains(@class, "_awwm2v")]/div/div[contains(@class, "_1kf6gff")]')
    data = []

    for result in results:
        try:
            temp_obj = {
                "name": 'Not Available',
                "category": 'Not Available',
                "address": 'Not Available',
                "link": 'Not Available',
            }
            name_element = result.find_element("xpath", './/div[contains(@class, "_zjunba")]//a[contains(@class, '
                                                        '"_1rehek")]')

            name = name_element.get_attribute("textContent").strip()
            temp_obj['name'] = name

            category_element = result.find_element("xpath", './/span[contains(@class, "_oqoid")]')
            category = category_element.get_attribute("textContent").strip()
            temp_obj['category'] = category

            address_element = result.find_element("xpath", './/span[contains(@class, "_1w9o2igt")]')
            address = address_element.get_attribute("textContent").strip()
            temp_obj['address'] = address

            link_element = result.find_element("xpath",
                                               './/div[contains(@class, "_zjunba")]//a[contains(@class, "_1rehek")]')
            link = link_element.get_attribute("href")
            temp_obj['link'] = link

            # print(temp_obj)
            data.append(temp_obj)
        except NoSuchElementException:
            # Skip this result if any required element is not found
            continue

    return data


# def save_checkpoint(company_num, page):
#     open("checkpoint.txt", "w").write(f"{company_num};{page}")
#
#
# def get_checkpoint():
#     global num
#     try:
#         if os.path.exists("checkpoint.txt"):
#             _ = open("checkpoint.txt", "r").read()
#             num = int(_.split(";")[0])
#             return int(_.split(";")[1])
#         else:
#             return 3
#     except Exception:
#         return 1


def main():
    global num
    global firm_info_list

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://2gis.ae/")
    time.sleep(3)
    query = 'barber shop in ajman'
    search_salons(query, driver)
    page_num = 0
    while True:
        data = parse_results(driver)
        extract_business_info(driver, data)
        store_csv(f'{query} - no dup.csv')
        # save_checkpoint(num, page_num)
        firm_info_list = []

        wait = WebDriverWait(driver, 100)
        buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._n5hmn94')))

        print(buttons)

        element = buttons[0]
        if len(buttons) >= 2:
            element = buttons[1]
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)
        page_num += 1
        print(driver.current_url)

    # page_num = get_checkpoint()
    # emirate = "ajman"
    # emirate = "ras%20al-khaimah"
    # emirate = "dubai"
    # emirate = "sharjah"
    # emirate = "fujairah"

    # while True:
    #
    #     url = f"https://2gis.ae/{emirate}/search/{query}/page/{page_num}"
    #     print(url)
    #     driver.get(url)
    #     time.sleep(4)  # Let the page load
    #     print(f"Opened page {page_num}")
    #     data = parse_results(driver)
    #     if not data:
    #         print(f"No more results on page {page_num}. Exiting...")
    #         break
    #
    #     extract_business_info(driver, data)
    #     store_csv(f'{query} - no dup.csv')
    #     save_checkpoint(num, page_num)
    #     firm_info_list = []
    #     page_num += 1
    #     time.sleep(3)

    # driver.quit()


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)
