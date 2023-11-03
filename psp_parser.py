import argparse
import sqlite3
import logging
import queries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sqlite3 import OperationalError
from time import sleep

CHROME_DRIVER_PATH = 'chromedriver-linux64/chromedriver'
PSP_URL = 'https://www.ameren.com/illinois/account/customer-service/bill/power-smart-pricing/prices'
PSP_DB = 'psp.db'
PSP_TABLE = 'psp'
LOG_FILE_PATH = 'psp.log'

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode='a',
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

def init_db():
    con = sqlite3.connect(PSP_DB)
    cur = con.cursor()
    try:
        logging.info('Attempting to create table if not exists')
        cur.execute(queries.get_create_table_query(PSP_TABLE))
        logging.info(f'Table created. Name={PSP_TABLE}')
    except OperationalError:
        logging.info('Table already exists, skipped creation')
    return con

def parse_psp(con, parse_tomorrow):
    price_map = {}

    options = Options()
    options.add_argument('headless')
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(PSP_URL)

    if parse_tomorrow:
        tomorrow_btn = driver.find_element(By.XPATH, '//*[@id="rtp-tomorrow"]')
        tomorrow_btn.click()
        sleep(5)

    table = driver.find_element(By.XPATH, '/html/body/div[2]/ameren-manage-program/ng-component/section/div/div/div[3]/div/div[4]/div/table/tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    if len(rows) != 24:
        logging.error(f'Incorrect number of rows parsed! Expect 24 but got {len(rows)}')
        exit()

    for h in range(0, 24):
        price_cent = rows[h].find_elements(By.TAG_NAME, 'td')[1].text[:-1]
        price_map[h] = price_cent
    try:
        cur = con.cursor()
        cur.execute(queries.get_insert_query(price_map))
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
