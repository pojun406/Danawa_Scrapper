from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome() # 드라이버 설정

RAM_url = 'http://prod.danawa.com/list/?cate=112752'
driver.get(RAM_url)
RAM_range = 34

driver.get(RAM_url)
data = []

# RAM 페이지 크롤링
for page in range(2, RAM_range):
    # 현재 페이지 출력
    print(f"Current Page: {page - 1}")
    # 스크롤 내리기
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩을 기다림
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product_list")))

    # 크롤링
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    product_li_tags = soup.select('li.prod_item.prod_layer')

    prod_list = [tag for tag in product_li_tags if 'product-pot' not in tag.get('class', [])]

    for li in prod_list:
        Brand_tmp = li.select_one('p.prod_name > a').text.strip().split(' ')
        Brand = Brand_tmp[0]
        name = li.select_one('p.prod_name > a').text.strip()
        spec_list = li.select_one('div.spec_list').text.strip().split(' / ')
        price_list = li.select('div.prod_pricelist')

        for price_item in price_list:
            prices = price_item.select('p.price_sect')
            sizes = price_item.select('p.memory_sect')

            for size, price_sect in zip(sizes, prices):
                size_text = size.get_text(strip=True).replace(',', " ").split('GB')
                if size_text and len(size_text) >= 2 and "원/" in size_text[0]:
                    size_text = size_text[1]
                    size_text = re.sub(r'^\d+위', '', size_text)
                else:
                    size_text = size_text[0]
                    size_text = re.sub(r'^\d+위', '', size_text)
                price_text = price_sect.select_one('a > strong').get_text(strip=True).replace(',', "")
                print(name, Brand, spec_list, size_text + "GB", price_text)

    # 페이지 버튼 클릭
    driver.execute_script("movePage(%d)" %page)