import requests
from bs4 import BeautifulSoup


# def get_euro():
#     url = 'https://www.cbr.ru/'
#     response = requests.get(url)
#     soup = response.text
#     src = BeautifulSoup(soup, 'lxml')
#     actually_EURO = src.find(class_='col-md-2 col-xs-9 _euro').find_next_sibling().text
#     exchange = float(actually_EURO.replace(',', '.').replace('₽', '').strip())
#     return exchange


def get_euro():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    response_content = response.content
    soup = BeautifulSoup(response_content, 'xml')
    exchange = soup.find(text='Евро').next.text
    return exchange

EURO_EXCHANGE = get_euro()








