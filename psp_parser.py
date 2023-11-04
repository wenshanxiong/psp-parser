import argparse
import sqlite3
import logging
import queries
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from sqlite3 import OperationalError
from time import sleep

PSP_URL = 'https://www.ameren.com/illinois/account/customer-service/bill/power-smart-pricing/prices'
LOG_FILE_PATH = 'psp.log'

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode='a',
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

def init_db():
    con = sqlite3.connect(queries.PSP_DB)
    cur = con.cursor()
    try:
        logging.info('Attempting to create table if not exists')
        cur.execute(queries.get_create_table_query(queries.PSP_TABLE))
        logging.info(f'Table created. Name={queries.PSP_TABLE}')
    except OperationalError:
        logging.info('Table already exists, skipped creation')
    return con

def parse_psp(con, parse_tomorrow):
    price_map = {}

    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(PSP_URL)

    if parse_tomorrow:
        tomorrow_btn = driver.find_element(By.XPATH, '//*[@id="rtp-tomorrow"]')
        tomorrow_btn.click()
        sleep(5)

    try:
        table = driver.find_element(By.XPATH, '/html/body/div[2]/ameren-manage-program/ng-component/section/div/div/div[3]/div/div[4]/div/table/tbody')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        date_text = driver.find_element(By.XPATH, '/html/body/div[2]/ameren-manage-program/ng-component/section/div/div/div[1]/span').text
        parsed_date = datetime.strptime(date_text, "Hourly Prices for %B %d, %Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
    except Exception:
        logging.exception('Failed to find price table')
        exit()

    if len(rows) != 24:
        logging.error(f'Incorrect number of rows parsed! Expect 24 but got {len(rows)}')
        exit()

    for h in range(0, 24):
        price_cent = rows[h].find_elements(By.TAG_NAME, 'td')[1].text[:-1]
        price_map[h] = price_cent
    try:
        print(price_map)
        cur = con.cursor()
        cur.execute(queries.get_insert_query(formatted_date, price_map))
        con.commit()
    except Exception:
        logging.exception('Error while inserting to DB')
    
    driver.quit()
    return price_map

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tomorrow", help="Parse tomorrow's prices",
                        action="store_true")
    args = parser.parse_args()

    con = init_db()
    parse_psp(con, args.tomorrow)
    con.close()

if __name__ == "__main__":
    main()
