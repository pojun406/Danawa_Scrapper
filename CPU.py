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

driver = webdriver.Chrome('chromedriver.exe')

#CPU-------------------------------------------------------------------
CPU_url = 'http://prod.danawa.com/list/?cate=112747'
driver.get(CPU_url)
CPU_range = 16
#RAM-------------------------------------------------------------------
RAM_url = 'http://prod.danawa.com/list/?cate=112752'
driver.get(RAM_url)
RAM_range = 34
#VGA-------------------------------------------------------------------
GVA_url = 'http://prod.danawa.com/list/?cate=112753'
driver.get(GVA_url)
GVA_range = 46
#MBoard-------------------------------------------------------------------
MBoard_url = 'http://prod.danawa.com/list/?cate=112751'
driver.get(MBoard_url)
MBoard_range = 46
#SSD-------------------------------------------------------------------
SSD_url = 'http://prod.danawa.com/list/?cate=112760'
driver.get(SSD_url)
SSD_range = 32
#HDD-------------------------------------------------------------------
HDD_url = 'http://prod.danawa.com/list/?cate=112763'
driver.get(HDD_url)
HDD_range = 18
#Power-------------------------------------------------------------------
Power_url = 'http://prod.danawa.com/list/?cate=112777'
driver.get(Power_url)
Power_range = 35
#Cooler-------------------------------------------------------------------
Cooler_url = 'http://prod.danawa.com/list/?cate=11236855'
driver.get(Cooler_url)
Cooler_range = 101
#Case-------------------------------------------------------------------
Case_url = 'http://prod.danawa.com/list/?cate=112775'
driver.get(Case_url)
Case_range = 49
#Moniter-------------------------------------------------------------------
Moniter_url = 'http://prod.danawa.com/list/?cate=112757'
driver.get(Moniter_url)
Moniter_range = 101



def CPUScrap():
    driver = webdriver.Chrome() # 드라이버 설정
    driver.get(CPU_url)
    data = []
    # CPU 페이지 크롤링
    for page in range(2, CPU_range):
        # 현재 페이지 출력
        print(f"Current Page: {page - 1}")
        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 페이지 로딩을 기다림
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product_list")))

        # 크롤링
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        product_li_tags = soup.select('li.prod_item.prod_layer')

        prod_list = [tag for tag in product_li_tags if 'product-pot' not in tag.get('class', [])]

        for li in prod_list:
            brand_tmp = li.select_one('p.prod_name > a').text.strip().split(' ')
            brand = brand_tmp[0]
            name = li.select_one('p.prod_name > a').text.strip()
            spec_list = li.select_one('div.spec_list').text.strip().split(' / ')
            try:
                price = li.select_one('li.rank_one > p.price_sect > a > strong').text.strip().replace(',',"")
            except:
                price = li.select_one('p.price_sect > a > strong').text.strip().replace(',',"")

            data.append({"name":name, "brand":brand, "spec":spec_list,"price":price})

        # 페이지 버튼 클릭
        driver.execute_script("movePage(%d)" %page)

        driver.close()

    with open('CPU_List.json','w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def RAMScrap():
    driver = webdriver.Chrome() # 드라이버 설정
    driver.get(RAM_url)
    data = []
    # RAM 페이지 크롤링
    for page in range(2, RAM_range):
        # 현재 페이지 출력
        print(f"Current Page: {page - 1}")
        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 페이지 로딩을 기다림
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product_list")))

        # 크롤링
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        product_li_tags = soup.select('li.prod_item.prod_layer')

        prod_list = [tag for tag in product_li_tags if 'product-pot' not in tag.get('class', [])]

        for li in prod_list:
            brand_tmp = li.select_one('p.prod_name > a').text.strip().split(' ')
            brand = brand_tmp[0]
            name = li.select_one('p.prod_name > a').text.strip()
            spec_list = li.select_one('div.spec_list').text.strip().split(' / ')
            try:
                price = li.select_one('input.value').text.strip().replace(',',"")
                size = li.select_one('p.memory_sect > #text')
            except:
                price = li.select_one('p.price_sect > a > strong').text.strip().replace(',',"")
                size = li.select_one('p.memory_sect > #text')

            data.append({"name":name, "brand":brand, "spec":spec_list,"price":price})

        # 페이지 버튼 클릭
        driver.execute_script("movePage(%d)" %page)

        driver.close()

    with open('RAM_List.json','w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
