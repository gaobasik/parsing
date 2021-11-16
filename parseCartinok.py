import requests
from bs4 import BeautifulSoup
from my_fake_useragent import UserAgent
import os
from datetime import datetime
import time
from random import uniform

def get_html(url, params=None):
    """html со страницы"""
    useragent = UserAgent().random()
    headers = {'user-agent':useragent}
    response = requests.get(url,headers=headers, params=params, timeout=20)
    html = response.text
    return html

def get_pages_count(html):
    soup = BeautifulSoup(html,'html.parser')
    try:
        pagination = soup.find('div',{'id':'clsLink3'})
        pages = pagination.get_text().split(' ')[-4].replace('>>','')
    except:
        print('Пагинация не найдена')
    print('Всего страниц: ' + str(pages))
    return int(pages)


def get_content(html):
    soup = BeautifulSoup(html,'lxml')
    block = soup.find('div',class_='block-photo')
    all_image = block.find_all('div',class_='short_full')
    name_type = [image.find('a').get('href') for image in all_image][0].split('/')[-2]
    #папка раздела
    if os.path.exists(f'image/{name_type}'):
        print(f"Продолжаю сохранять в папку:'{name_type}':")
        pass
    else:
        os.mkdir(f'image/{name_type}')
        print(f"Папка '{name_type}' создана!")
    domen = 'https://zastavok.net'

    #изображения
    for image in all_image:
        image_page = domen + image.find('a').get('href')
        image_name = image.find('img').get('alt')
        download_storage = requests.get(f'{image_page}').text
        download_soup = BeautifulSoup(download_storage,'lxml')
        #ссылка на высокое разрешение(если нужно расскоменть)
       # download_block = download_soup.find('div',class_='block_down')
        #image_link = domen + download_block.find('a').get('href')
        #ссылка на низкое разрешение
        download_block = download_soup.find('div',class_='main_image')
        image_link = domen + download_block.find('img').get('src')

        #изображение в байтах
        image_bytes = requests.get(f'{image_link}').content
        #проверка на существ такого изображения в папке
        if os.path.exists(f'image/{name_type}/{image_name}.jpg'):
            print(f"Было скачено ранее: '{image_name}'")
        else:
            #Сохраняем полученное изображение
            with open(f'image/{name_type}/{image_name}.jpg','wb') as file:
                file.write(image_bytes)
                print(f"Успешно скачено изображение: '{image_name}'!")
        time.sleep(uniform(1,2))


def parser(url):
    #оСНОВНАЯ ФУНКЦИЯ ПАРСЕРА
    try:
        html = get_html(url)
        pages = get_pages_count(html)
        #пока все условия не выполняться, все будет повторяться
        while True:
                lists = pages
                page = int(input('Введите страницу с которой начать:'))
                if page >= int(pages):
                    print(f'Введите число меньше, чем общее количество страниц({pages})')
                else:
                    pages = int(input('Введите страницу на которой закончить: '))
                    if pages <= page:
                        print(f'Неверный диапазон,стартовая граница - {page},больше конечной')
                    elif pages >= lists:
                        print(f'Вы ввели число больше,чем общее количество листов({lists})')
                    else:
                        start = datetime.now()
                        for page in range(1,pages+1):
                            print(f"Скачивание со страницы {page}...")
                            html = get_html(url+f'/{page}')
                            get_content(html)
                        end = datetime.now()
                        total = end - start
                        print("Затраченной время:" + str(total))
                        break

        print('Скачивание изображений прошло успешно')
    except Exception as ex:
            print(f'Что то пошло не так! Ошибка:\n {ex}')



parser('https://zastavok.net/games/')
        
