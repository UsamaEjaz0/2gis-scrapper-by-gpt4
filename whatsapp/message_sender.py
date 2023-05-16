import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from urllib.parse import quote

options = Options()

f = open("/Users/usamaejaz/Desktop/Uniform Business/2gis-scrapper/whatsapp/message.txt", "r")
message = f.read()
f.close()

message = quote(message)

numbers = []
f = open("/Users/usamaejaz/Desktop/Uniform Business/2gis-scrapper/whatsapp/numbers.txt", "r")
for line in f.read().splitlines():
    if line.strip() != "":
        numbers.append(line.strip())
f.close()
total_number = len(numbers)

print('We found ' + str(total_number) + ' numbers in the file')
delay = 10

driver = webdriver.Chrome(options=options)

print('Once your browser opens up sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
input("After logging into WhatsApp Web is complete and your chats are visible, press ENTER...")

for idx, number in enumerate(numbers):
    number = number.strip()
    if number == "":
        continue
    print('{}/{} => Sending message to {}.'.format((idx + 1), total_number, number))
    try:
        url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message

        driver.get(url)
        try:

            clip_btn = WebDriverWait(driver, delay).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-testid='clip']")))
            clip_btn.click()

            sleep(1)

            # Locate the file input element and send the video file path
            file_input = driver.find_element(By.XPATH,
                                             "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
            file_input.send_keys("/Users/usamaejaz/Desktop/Uniform Business/2gis-scrapper/whatsapp/Test.mov")

            sleep(5)
            send_btn = WebDriverWait(driver, delay).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-testid='send']")))
            # Scroll the send button into view
            actions = ActionChains(driver)
            actions.move_to_element(send_btn).perform()
            sleep(1)
            send_btn.click()
            sleep(3)
            print('Message sent to: ' + number)
        except Exception as e:
            print("Encountered problem with", number)
            print(e)
    except Exception as e:
        print('Failed to send message to ' + number, str(e))
driver.close()
