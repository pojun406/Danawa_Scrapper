from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = 'https://prod.danawa.com/list/?cate=112747'
driver.get(url)

for page in range(1, 16):
    while True:
        try:
            xpath = f'//div.number_wrap//a[contains(@onclick, {page})]'
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            next_page = driver.find_element_by_xpath(xpath)
            next_page.click()
            break
        except NoSuchElementException:
            pass

    print(f'Page {page}:')

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_li_tags = soup.select('li.prod_item.prod_layer')

    for li in product_li_tags:
        name = li.select_one('p.prod_name > a').text.strip()
        spec_list = li.select_one('div.spec_list').text.strip()
        price = li.select_one('li.rank_one > p.price_sect > a > strong').text.strip().replace(',', '')
        print(name, spec_list, price)
