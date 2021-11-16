import requests
import csv
from bs4 import BeautifulSoup as BS

URL = "https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CGA9M2X7R1E106M200KA"
HEADERS = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36", 'accept': '*/*'}


def get_html(url,params=None):
 r = requests.get(URL, headers = HEADERS, params=params)   
 return r

def get_content(html):
     soup = BS(html,'lxml')
     all =  soup.find_all('table',class_="spec_table electrical_characteristics")
     print(all)
     return all

print(all)



     
     