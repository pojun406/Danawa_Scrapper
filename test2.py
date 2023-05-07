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
url = 'https://prod.danawa.com/list/?cate=112747'
driver.get(url)
#15페이지
for page in range(1, 16):
    # xpath = f'//div.number_wrap//a[contains(@onclick, "{page}")]'
    # next_page = driver.find_element_by_xpath(xpath)
    # driver.execute_script("arguments[0].scrollIntoView();", next_page)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//div.number_wrap//a[contains(@onclick, {page})]')))
    next_page = driver.find_element_by_xpath(f'//div.number_wrap//a[contains(@onclick, {page})]')
    time.sleep(5)
    print(page)
    soup = BeautifulSoup(driver.page_source)
    product_li_tags = soup.select('li.prod_item.prod_layer')
    product_page_tags = soup.select('div.number_wrap')
    print(len(product_li_tags))
    for li in product_li_tags:
        name = li.select_one('p.prod_name > a').text.strip()
        spec_list = li.select_one('div.spec_list').text.strip()
        price = li.select_one('li.rank_one > p.price_sect > a > strong').text.strip().replace(',',"")
        print(name, spec_list, price)
    # driver.execute_script("arguments[0].click();", next_page)
    next_page.click()