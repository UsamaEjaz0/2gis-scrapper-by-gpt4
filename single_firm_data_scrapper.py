import pandas as pd
from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options

skipped = 0

def get_output_df(output_file_path):
    if os.path.exists(output_file_path):
        df_out = pd.read_csv(output_file_path)
    else:
        df_out = pd.DataFrame(
            columns=["Name", "Given Name", "Additional Name", "Family Name", "Yomi Name", "Given Name Yomi",
                     "Additional Name Yomi", "Family Name Yomi", "Name Prefix", "Name Suffix", "Initials",
                     "Nickname", "Short Name", "Maiden Name", "Birthday", "Gender", "Location",
                     "Billing Information", "Directory Server", "Mileage", "Occupation", "Hobby",
                     "Sensitivity", "Priority", "Subject", "Notes", "Language", "Photo", "Group Membership",
                     "E-mail 1 - Type", "E-mail 1 - Value", "Phone 1 - Type", "Phone 1 - Value",
                     "Phone 2 - Type", "Phone 2 - Value", "Organization 1 - Type", "Organization 1 - Name",
                     "Organization 1 - Yomi Name", "Organization 1 - Title", "Organization 1 - Department",
                     "Organization 1 - Symbol", "Organization 1 - Location",
                     "Organization 1 - Job Description"])

    return df_out


def to_csv_individual_firm_data(driver, output_file_path, input_file_path):
    global firm_info_list
    global skipped

    num, saved_index = get_checkpoint()

    if os.path.exists(input_file_path):
        df = pd.read_csv(input_file_path)
        for index, row in df.iterrows():
            if index > saved_index:
                try:
                    df_out = get_output_df(output_file_path)
                    driver.get(row['link'])
                    time.sleep(2)
                    phone_element = driver.find_element("xpath", '//a[contains(@href, "tel:")]')
                    phone_number = phone_element.get_attribute('href').split(':')[1].strip()

                    entry = {
                        "Name": "GS " + str(num) + " " + row['name'],
                        "Given Name": "GS " + str(num) + " " + row['name'],
                        "Phone 1 - Type": "Mobile",
                        "Phone 1 - Value": f"{phone_number}",
                        "Organization 1 - Name": row["name"],
                        # "Location": row["address"],
                        # "Notes": row["link"]
                    }

                    print(f"{entry['Name']} inserted")
                    num += 1

                    df_out = df_out._append(entry, ignore_index=True)
                    df_out.to_csv(output_file_path, index=False)
                    save_checkpoint(num, index)


                except Exception as e:
                    print(f"Error in {skipped} entry(s): {e}")
                    skipped += 1
                    continue

    else:
        print("Make sure there's a transitional_df.csv file in the resources.")


def save_checkpoint(company_num, index):
    open("resources/checkpoint.txt", "w").write(f"{company_num};{index}")


def get_checkpoint():
    global num
    try:
        if os.path.exists("resources/checkpoint.txt"):
            _ = open("resources/checkpoint.txt", "r").read()
            num = int(_.split(";")[0])
            index = int(_.split(";")[1])

            return num, index
        else:
            return 1, 0
    except Exception:
        return 1, 0


def main():

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    phone_numbers_path = f"resources/numbers.csv"
    transitional_df_path = "resources/transitional_df.csv"

    to_csv_individual_firm_data(driver, phone_numbers_path, transitional_df_path)


if __name__ == "__main__":
    main()
