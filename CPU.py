import os
import sys

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(executable_path="C:/Users/byung/Documents/GitHub/Danawa_Scrapper/chromedriver.exe",
                          options=options)
url = 'https://prod.danawa.com/list/?cate=112747'
driver.get(url)
data = []
CPU_range = 10

for page in range(2, CPU_range):
    # 현재 페이지 출력
    print(f"Current Page: {page - 1}")
    time.sleep(3)

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩을 기다림
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product_list")))

    # 크롤링
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    product_li_tags = soup.select('li.prod_item.prod_layer')
    prod_list = [tag for tag in product_li_tags if 'product-pot' not in tag.get('class', [])]

    for li in prod_list:
        # img = li.select_one('div.thumb_image > a > img').text.strip()
        '''img = li.select_one('img')
        if img:
            img_src = img.get('src')
            print(img_src)'''
        img_link = li.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = li.select_one('div.thumb_image > a > img').get('src')
        img_link = img_link.replace("shrink=130:130", "shrink=330:*")
        name = li.select_one('p.prod_name > a').text.strip()
        brand_tmp = li.select_one('p.prod_name > a').text.strip().split(' ')
        brand = brand_tmp[0]
        spec_list = li.select_one('div.spec_list').text.strip().split(' / ')
        try:
            price = li.select_one('li.rank_one > p.price_sect > a > strong').text.strip().replace(',', "")
        except:
            price = li.select_one('p.price_sect > a > strong').text.strip().replace(',', "")
        print(name, spec_list, price, img_link)
        data.append({"name": name, "brand": brand, "spec": spec_list, "price": price, "img": img_link, "Cate": "CPU"})

# 결과 파일 경로 설정
file_path = os.path.abspath('HARDWARE_DATA_old/CPU_List.json')

# 결과 파일 저장
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # WebDriver 종료
    driver.quit()

    # 스크립트 강제 종료
    sys.exit()
