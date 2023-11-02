from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('headless')
DRIVER_PATH = 'chromedriver_mac_arm64/chromedriver'
PSP_URL = 'https://www.ameren.com/illinois/account/customer-service/bill/power-smart-pricing/prices'

price_map = {}

driver = webdriver.Chrome(options=options)
driver.get(PSP_URL)
table = driver.find_element(By.XPATH, '/html/body/div[2]/ameren-manage-program/ng-component/section/div/div/div[3]/div/div[4]/div/table/tbody')
rows = table.find_elements(By.TAG_NAME, 'tr')
assert(len(rows) == 24)
for h in range(0, 24):
    price_cent = rows[h].find_elements(By.TAG_NAME, 'td')[1].text[:-1]
    price_map[h] = price_cent
print(price_map)
driver.quit()

