import requests
from bs4 import BeautifulSoup
import time
import csv


url = 'https://fsa.gov.ru/press-center/info/'

headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

def pagination():
    url = 'https://fsa.gov.ru/press-center/info/'
    r = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    article_list = []
    result_data = []

    with open('practic.csv','w',encoding='cp1251') as file:
        writer = csv.writer(file,delimiter = ';')
        writer.writerow(
            (
                'Ссылка',
                'Название',
                'Дата'
                
            )
        )
    pagenat = int(soup.find('div',class_='pagination__list').find_all('a')[-1].text)
    for page in range(1,pagenat - 1):
        responce = requests.get(url = f'https://fsa.gov.ru/press-center/info/?PAGEN_1={page}&SIZEN_1=10',headers=headers)
        linksoup = BeautifulSoup(responce.text,'lxml')
        time = linksoup.find_all('div',class_='news-item__info-item')
        for data in time:
            data = data.text.strip()
            
        title = linksoup.find_all('a',class_='news-item__title-link')
        for href in title:
            href = href.get('href')
            
        for name in title:
            name = name.text.strip()
        
        with open('practic.csv','a',encoding='UTF-8') as file:
            writer = csv.writer(file,delimiter = ';')
            writer.writerow(
                (
                    f'https://fsa.gov.ru/' + href,
                    name,
                    data
                )
            )
        print(f'Обработал {page}...')




     
            
     
      
     


       
        
      
     #title = linksoup.find('div',class_='container').find_all('div',class_='list-item__item')
    # for text in title:
        # name =  text.find('a',class_='news-item__title-link').text.strip()
         

     
     
     
     




def main():
    pagination()

if __name__ == "__main__":
    main()
