from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

data = []

driver = webdriver.Chrome()
url = 'http://prod.danawa.com/list/?cate=112753'
driver.get(url)
VGA_range = 46

for page in range(2, VGA_range):
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
        img_link = li.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = li.select_one('div.thumb_image > a > img').get('src')
        Brand_tmp = li.select_one('p.prod_name > a').text.strip().split(" ")
        Brand = Brand_tmp[0]
        name = li.select_one('p.prod_name > a').text.strip()
        spec_list = li.select_one('div.spec_list').text.strip().split(' / ')
        price = li.select_one('p.price_sect > a > strong').text.strip().replace(',',"")
        data.append({"name":name, "brand":Brand, "spec":spec_list,"price": price, "img":img_link})

    # 페이지 버튼 클릭
    driver.execute_script("movePage(%d)" %page)

with open('HARDWARE_DATA/VGA_List.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
