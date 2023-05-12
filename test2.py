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

# 15 페이지까지 크롤링
for page in range(2, 16):
    # 현재 페이지 출력
    print(f"Current Page: {page - 1}")

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)


    # 페이지 로딩을 기다림
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product_list")))

    # 크롤링
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    product_li_tags = soup.select('li.prod_item.prod_layer')
    print(len(product_li_tags))
    for li in product_li_tags:
        name = li.select_one('p.prod_name > a').text.strip()
        spec_list = li.select_one('div.spec_list').text.strip()
        try :
            price = li.select_one('li.rank_one > p.price_sect > a > strong').text.strip().replace(',',"")
        except :
            price = li.select_one('p.price_sect > a > strong').text.strip().replace(',',"")
        print(name, spec_list, price)

    # 페이지 버튼 클릭
    driver.execute_script("movePage(%d)" %page)
