from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import time
from tqdm import tqdm_notebook

import pandas as pd
import numpy as np

driver = webdriver.Chrome('chromedriver.exe')

#CPU
CPU_url = 'http://prod.danawa.com/list/?cate=112747'
driver.get(CPU_url)
'''
#RAM
RAM_url = 'http://prod.danawa.com/list/?cate=112752'
driver.get(RAM_url)
#VGA
GVA_url = 'http://prod.danawa.com/list/?cate=112753'
driver.get(GVA_url)
#MBoard
MBoard_url = 'http://prod.danawa.com/list/?cate=112751'
driver.get(MBoard_url)
#SSD
SSD_url = 'http://prod.danawa.com/list/?cate=112760'
driver.get(SSD_url)
#HDD
HDD_url = 'http://prod.danawa.com/list/?cate=112763'
driver.get(HDD_url)
#Power
Power_url = 'http://prod.danawa.com/list/?cate=112777'
driver.get(Power_url)
#Cooler
Cooler_url = 'http://prod.danawa.com/list/?cate=11236855'
driver.get(Cooler_url)
#Case
Case_url = 'http://prod.danawa.com/list/?cate=112775'
driver.get(Case_url)
#Moniter
Moniter_url = 'http://prod.danawa.com/list/?cate=112757'
driver.get(Moniter_url)
'''

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
prod_items = soup.select('div.main_prodlist > ul > li')

for item in prod_items:
    try:
        title = item.select('a.click_log_product_standard_title_')[0].text.strip()
        spec = item.select('div.spec_list')[0].text.strip()
        price = item.select('li.rank_one > p.price_sect > a > strong')[0].text.strip().replace(",","")
        print(title, spec, price)
    except:
        continue


'''
prod_items[0].select('a.click_log_product_standard_title_')[0].text
title = prod_items[0].select('p.prod_name > a')[0].text
spec_list = prod_items[0].select('div.spec_list')[0].text.strip()
price = prod_items[0].select('li.rank_one > p.price_sect > a > strong')[0].text.strip().replace(",","")
print(title, spec_list, price, sep='    |||    ')
'''