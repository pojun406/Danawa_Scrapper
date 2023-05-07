from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm_notebook
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np
import json

driver = webdriver.Chrome()

url = 'https://prod.danawa.com/list/?cate=112747&shortcutKeyword=CPU'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
prod_items = soup.select('div.main_prodlist > ul.product_list > li.prod_item')
title = prod_items[0].select('p.prod_name > a')[0].text

spec_list = prod_items[0].select('div.spec_list')[0].text.strip()
price = prod_items[0].select('li.rank_one > p.price_sect > a > strong')[0].text.strip().replace(',', "")
#print(title, spec_list, price + "원", sep='    |||    ')

'''
# try: except: 구문으로 태그내 광고 제거
prod_data = []

for prod_item in prod_items:
    try:
        title = prod_item.select('p.prod_name > a')[0].text
    except:
        title = ""
    try:
        spec_list = prod_item.select('div.spec_list')[0].text.strip()
    except:
        title = ""
    try:
        price = prod_item.select('li.rank_one > p.price_sect > a > strong')[0].text.strip().replace(',', "")
    except:
        price = 0
    mylist = [title, spec_list, price]
    prod_data.append(mylist)

for data in prod_data[:5]:
    print(data)
'''


def get_prod_items(prod_items):
    prod_data = []

    for prod_item in prod_items:
        try:
            title = prod_item.select('p.prod_name > a')[0].text
        except:
            title = ""
        try:
            spec_list = prod_item.select('div.spec_list')[0].text.strip()
        except:
            title = ""
        try:
            price = prod_item.select('li.rank_one > p.price_sect > a > strong')[0].text.strip().replace(',', "")
        except:
            price = 0
        mylist = [title, spec_list, price]
        prod_data.append(mylist)
    return (prod_data)

prod_data = get_prod_items(prod_items)
print(len(prod_data))
print(prod_data)
