from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import json

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome('chromedriver', options=options)

Case_url = 'http://prod.danawa.com/list/?cate=112775'
driver.get(Case_url)
Case_range = 46

excluded_items = ["HDD (NAS용)", "쿼드로", "고정핀/나사", "VGA 지지대", "써멀패드", "SSD/HDD 주변기기", "임베디드 보드", "방열판", "제온", "중고",
                  "VR 지원 장비", "PowerLink", "SLI Bridge", "노트북", "노트북용", "전용 액세서리", "외장그래픽 독", "HDD (CCTV용)", "DC to DC",
                  "중고 여부 확인요망", "RAM 쿨러", "구매 시 주의사항: 쿨링팬 수(선택), OC(선택), 채굴 여부 판매자 별도 문의 요망", "가이드", "서버용 파워", "서버용",
                  "수랭 부속품", "오일", "인텔(CPU내장)", "조명기기", "채굴용 케이스", "케이블", "튜닝 부속품", "팬 부속품", "팬컨트롤러", "서버용 파워",
                  "제품 상세 정보는 판매중인 쇼핑몰에서 반드시 확인하시기 바랍니다", "DDR2", "방열판 분류용 상품"]

data = []

for page in range(2, Case_range):
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
                data.append({"name":name, "brand":Brand, "spec":spec_list,"color_text" : color_text, "price": price_text, "img":img_link, "Cate":"Case"})

# 페이지 버튼 클릭
    driver.execute_script("movePage(%d)" %page)
with open('HARDWARE_DATA_old/Case_List.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)