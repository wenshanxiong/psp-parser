from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
import logging
from sqlite3 import OperationalError
import queries

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

def parse_psp(con):
    price_map = {}

    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    driver.get(PSP_URL)
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
    con = init_db()
    parse_psp(con)
    con.close()

if __name__ == "__main__":
    main()
