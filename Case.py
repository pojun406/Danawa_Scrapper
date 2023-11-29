import sys

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import json
import os

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(executable_path="C:/Users/byung/Documents/GitHub/Danawa_Scrapper/chromedriver.exe", options=options)

Case_url = 'http://prod.danawa.com/list/?cate=112775'
driver.get(Case_url)
Case_range = 10
data = []

for page in range(2, Case_range):
    # 현재 페이지 출력
    print(f"Current Page: {page - 1}")
    time.sleep(5)  # 좀 더 긴 시간으로 변경

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩을 기다림
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product_list")))

    # 크롤링
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    product_li_tags = soup.select('li.prod_item.prod_layer')
    prod_list = [tag for tag in product_li_tags if 'product-pot' not in tag.get('class', [])]

    for li in prod_list:
        img_link = li.select_one('div.thumb_image > a > img').get('data-original')
        if img_link is None:
            img_link = li.select_one('div.thumb_image > a > img').get('src')
        img_link = img_link.replace("shrink=130:130", "shrink=330:*")
        Brand_tmp = li.select_one('p.prod_name > a').text.strip().split(" ")
        Brand = Brand_tmp[0]
        name = li.select_one('p.prod_name > a').text.strip()
        spec_list = li.select_one('div.spec_list').text.strip().split(' / ')
        price_list = li.select('div.prod_pricelist')

        for price_item in price_list:
            prices = price_item.select('p.price_sect')
            colors = price_item.select('p.memory_sect')
            for color, price_sect in zip(colors, prices):
                color_text = color.get_text(strip=True).strip()
                color_text = re.sub(r'^\d+위', '', color_text)
                price_text = price_sect.select_one('a > strong').get_text(strip=True).replace(',', "")
                print(name, Brand, spec_list, color_text, price_text)
                data.append({"name": name, "brand": Brand, "spec": spec_list, "color_text": color_text, "price": price_text, "img": img_link, "Cate": "Case"})

    # 페이지 버튼 클릭
    driver.execute_script("movePage(%d)" % page)

# 결과 파일 경로 설정
file_path = os.path.abspath('HARDWARE_DATA_old/Case_List.json')

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