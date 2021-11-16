import requests
from bs4 import BeautifulSoup
import pandas
from pandas import ExcelWriter
import openpyxl
import lxml



HEADERS = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36", 'accept': '*/*'}
#URL = 'https://www.wildberries.ru/brands/xiaomi/all'
def get_html(url,params=None):
    responce = requests.get(url=url,headers=HEADERS,params=params)
    html = responce.text
    return html


def get_pages(html):
    soup = BeautifulSoup(html,'lxml')
    good_count = soup.find('span',class_="goods-count").get_text(strip=True).replace('\xa0', '').split()[0]
    pages = int(good_count) // 100 + 1
    return pages

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="product-card")
    cards = []
    for item in items:
        # проверка на наличии скидки, если нет, то поле пустое
        discount = item.find('span', class_='product-card__sale')
        if discount:
            discount = discount.get_text(strip=True)
        else:
            discount = ''
        try:

            price  = int(item.find(class_='price-commission__price-free-commission').get_text(strip=True).replace('\xa0', '').replace('₽', '')),
            
        except:
            price = 0
     
        cards.append({
            'brand': item.find('strong', class_='brand-name').get_text(strip=True).replace('/', ''),
            'title': item.find('span', class_='goods-name').get_text().split('/')[0],
            'price':price,
            'discount': discount,
            'link': f'https://www.wildberries.ru{item.find("a", class_="product-card__main").get("href")}',
        })
       
    return cards
def save_exel(data):
    # сохраняем полученные данные в эксель с помощью dataframe от pandas
    dataframe = pandas.DataFrame(data)
    newdataframe = dataframe.rename(columns={'brand': 'Брэнд', 'title': 'Наименование',
                                             'price': 'Цена',  'discount': 'Скидка',
                                             'link': 'Ссылка'})
    writer = ExcelWriter(f'data.xlsx')
    newdataframe.to_excel(writer, 'data')
    writer.save()
    print(f'Данные сохранены в файл "data.xlsx"')

def parse(url):
    global search
    search = url
    print(f'Парсим данные с: "{search}"')
    html = get_html(url)
    pages = get_pages(html)
    print(f'Количество страниц: {pages}')
    cards = []
    pages = int(input('Введите количество страниц: '))
    for page in range(1, pages + 1):
        print(f'Парсинг страницы: {page}')
        html = get_html(url, params={'sort': 'popular', 'page': page})
        cards.extend(get_content(html))
    print(f'Всего: {len(cards)} позиций')
    save_exel(cards)











if __name__ == "__main__":
    parse('https://www.wildberries.ru/brands/xiaomi/all')