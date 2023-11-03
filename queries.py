from sqlite3 import Date
from psp_parser import PSP_TABLE

def get_create_table_query(table_name):
    return f"""
CREATE TABLE {table_name} (
    date TEXT UNIQUE CHECK (date LIKE '____-__-__'),
    "0" REAL,
    "1" REAL,
    "2" REAL,
    "3" REAL,
    "4" REAL,
    "5" REAL,
    "6" REAL,
    "7" REAL,
    "8" REAL,
    "9" REAL,
    "10" REAL,
    "11" REAL,
    "12" REAL,
    "13" REAL,
    "14" REAL,
    "15" REAL,
    "16" REAL,
    "17" REAL,
    "18" REAL,
    "19" REAL,
    "20" REAL,
    "21" REAL,
    "22" REAL,
    "23" REAL
);
"""

def get_insert_query(price_map):
    return f"""
INSERT INTO {PSP_TABLE} VALUES (
    '{str(Date.today())}',
    {price_map[0]},  
    {price_map[1]},
    {price_map[2]},
    {price_map[3]},
    {price_map[4]},
    {price_map[5]},
    {price_map[6]},
    {price_map[7]},
    {price_map[8]},
    {price_map[9]},
    {price_map[10]},
    {price_map[11]},
    {price_map[12]},
    {price_map[13]},
    {price_map[14]},
    {price_map[15]},
    {price_map[16]},
    {price_map[17]},
    {price_map[18]},
    {price_map[19]},
    {price_map[20]},
    {price_map[21]},
    {price_map[22]},
    {price_map[23]}
);
"""
