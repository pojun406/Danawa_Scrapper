from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

HDD_url = 'http://prod.danawa.com/list/?cate=112763'
driver.get(HDD_url)
HDD_range = 18

data = []
for page in range(2, HDD_range):
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
        price_list = li.select('div.prod_pricelist')
        for price_item in price_list:
            prices = price_item.select('p.price_sect')
            sizes = price_item.select('p.memory_sect')
            size_TorG_tmp = ['TB','GB']

            for size, price_sect in zip(sizes, prices):
                size_text = size.get_text(strip=True).replace(' ', "")
                if 'TB' in size_text:
                    size_tmp = 'TB'
                    size_text = size_text.split('TB')
                elif 'GB' in size_text:
                    size_tmp = 'GB'
                    size_text = size_text.split('GB')
                else:
                    size_tmp = ''

                if(size_tmp == 'TB'):
                    size_cut_tmp = size_text[0] # 이미 TB를 썰어서 배열로 가져옴
                    size_cut_com = size_cut_tmp.split(',') # 썰어온 size_text를 다시 ,로 썲
                    try:
                        size_text = size_cut_com[1]
                        size_TorG = [size_text,size_tmp]
                    except:
                        size_text = size_cut_com[0]
                        size_TorG = [size_text,size_tmp]
                else:
                    size_cut_tmp = size_text[0]
                    if '/' in size_text[0]: # 만약 '/'가 첫번째에 있을경우 size_text는 2다
                        size_cut_tmp = size_text[1]
                    else:
                        size_cut_tmp = size_text[0]
                    size_cut_com = size_cut_tmp.split(',')
                    try:
                        size_text = size_cut_com[1]
                        size_TorG = [size_text,size_tmp]
                    except:
                        size_text = size_cut_com[0]
                        size_TorG = [size_text,size_tmp]

                price_text = price_sect.select_one('a > strong').get_text(strip=True).replace(',', "")

                print(name, Brand, spec_list, size_TorG, price_text)
                data.append({"name":name, "brand":Brand, "spec":spec_list,"size" : size_TorG, "price": price_text, "img":img_link})

# 페이지 버튼 클릭
    driver.execute_script("movePage(%d)" %page)

with open('./HARDWARE_DATA/HDD_List.json','w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)