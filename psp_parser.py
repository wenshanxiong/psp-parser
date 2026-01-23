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
from logging.handlers import RotatingFileHandler

PSP_URL = 'https://www.ameren.com/illinois/account/customer-service/bill/power-smart-pricing/prices'
LOG_FILE_PATH = 'psp.log'

logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
log_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5*1024*1024, backupCount=1)  # max size is 5MB, keep 1 backup
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

def init_db():
    con = sqlite3.connect(queries.PSP_DB)
    cur = con.cursor()
    try:
        logger.info('Attempting to create table if not exists')
        cur.execute(queries.get_create_table_query(queries.PSP_TABLE))
        logger.info(f'Table created. Name={queries.PSP_TABLE}')
    except OperationalError:
        logger.info('Table already exists, skipped creation')
    return con

def parse_psp(con, parse_tomorrow, parse_yesterday):
    price_map = {}

    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(PSP_URL)
    
    # Set preferred state cookie
    driver.add_cookie({'name': 'PreferredState', 'value': 'en-US-il'})
    driver.refresh()
    sleep(2)

    if parse_tomorrow:
        logger.info("Navigating to tomorrow's price")
        tomorrow_btn = driver.find_element(By.XPATH, '//*[@id="rtp-tomorrow"]')
        tomorrow_btn.click()
        sleep(5)
    elif parse_yesterday:
        logger.info("Navigating to yesterday's price")
        yesterday_btn = driver.find_element(By.XPATH, '//*[@id="rtp-previous-day"]')
        yesterday_btn.click()
        sleep(5)

    try:
        table = driver.find_element(By.XPATH, '/html/body/div[2]/ameren-manage-program/ng-component/section/div/div/div[3]/div/div[4]/div/table/tbody')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        date_text = driver.find_element(By.XPATH, '/html/body/div[2]/ameren-manage-program/ng-component/section/div/div/div[1]/span').text
        parsed_date = datetime.strptime(date_text, "Hourly Prices for %B %d, %Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
    except Exception:
        logger.exception('Failed to find price table')
        exit()

    if len(rows) != 24:
        logger.error(f'Incorrect number of rows parsed! Expect 24 but got {len(rows)}')
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
        logger.exception('Error while inserting to DB')
    
    driver.quit()
    return price_map

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tomorrow", help="Parse tomorrow's prices",
                        action="store_true")
    parser.add_argument("-y", "--yesterday", help="Parse yesterday's prices",
                        action="store_true")
    args = parser.parse_args()

    con = init_db()
    parse_psp(con, args.tomorrow, args.yesterday)
    con.close()

if __name__ == "__main__":
    main()
