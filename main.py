import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
import pandas as pd


def get_euro():
    url = 'https://www.cbr.ru/'
    response = requests.get(url)
    soup = response.text
    src = BeautifulSoup(soup, 'lxml')
    actually_EURO = src.find(class_='col-md-2 col-xs-9 _euro').find_next_sibling().text
    number = float(actually_EURO.replace(',', '.').replace('₽', '').strip())
    return number


options = webdriver.ChromeOptions()

# dusable web driver
options.add_argument("--disable-blink-features=AutomationControlled")

# headless mode
options.add_argument("--headless")

# driver = webdriver.Chrome(service=Service('C:\\Users\\Марк\\Desktop\\avito scrap\\chromedriver.exe'), options=options)
 driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
     "source": """
          const newProto = navigator.__proto__
          delete newProto.webdriver
          navigator.__proto__ = newProto
          """
    })

EURO = get_euro()
data = []

url = f'https://www.avito.ru/moskva/telefony'
driver.get(url=url)
items = driver.find_elements(
    by=By.XPATH, value="//div[@data-marker='item-photo']"
)

for item in items:
    item.click()
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[1])
    page_html = BeautifulSoup(driver.page_source, 'lxml')

    item_url = str(driver.current_url)
    try:
        item_id = page_html.find("span", {"data-marker": "item-view/item-id"}) \
            .text.strip()
        
    except Exception as e:
        print(e)
        item_id = 'No data'

    try:
        title = page_html.find("span", {"class": "title-info-title-text"}) \
            .text.strip()
    except Exception as e:
        print(e)
        title = 'No data'

    try:
        price_html = page_html.find("span", {"class": "js-item-price"})
        price_rub = price_html['content']
        price_eur = round(float(price_rub) / float(EURO), 2)

    except Exception as e:
        print(e)
        price_eur = 'No data'

    try:
        publicate_date = page_html.find(
            "div", {"class": "title-info-metadata-item-redesign"}
        ).text.strip()
    except Exception as e:
        print(e)
        publicate_date = 'No data'

    try:
        html_characteristics = [item.text.split(':') for item in page_html.find("ul", {"class": "item-params-list"})]
        characteristics = ' '.join([item[-1].strip() for item in html_characteristics if item])
    except Exception as e:
        print(e)
        characteristics = 'No data'

    try:
        description = page_html.find("div", {"class": "item-description-text"}) \
            .text.strip()
    except Exception as e:
        print(e)
        description = 'No data'

    try:
        address = page_html.find("span", {"class": "item-address__string"}) \
            .text.strip()
    except Exception as e:
        print(e)
        address = 'No data'

    data_page = (item_url, item_id, title, price_eur, publicate_date,
                 characteristics, description, address)
    data.append(data_page)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print('Page processed.')

print('Create date base')

try:
    connection = sqlite3.connect('avito.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS avito_data (
                                        id INTEGER PRIMARY KEY,
                                        url TEXT,
                                        ID_item INT,
                                        title TEXT,
                                        price_eur TEXT,
                                        publicate_date TEXT,
                                        characteristics TEXT,
                                        description TEXT,
                                        address TEXT
                                        );'''
                   )
    connection.commit()

    cursor.executemany("""INSERT INTO avito_data
                                  VALUES (NULL, ?, ?, 
                                            ?, ?, ?,
                                            ?, ?, ?)""", data)


    connection.commit()

    df = pd.read_sql('select * from avito_data', connection)
    df.to_excel(r'result.xlsx', index=False)

    cursor.close()
    print('Successfully!')
except Exception as e:
    print(f'Error is {e}')


