#coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

start_url = 'https://www.120ask.com'


headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]

def get_chennel_urls(url):


    wb_data = requests.get(start_url, timeout =30,headers = random.choice(headers_pool))
    wb_data.raise_for_status

    # 进行了手动测试编码，并设置好
    wb_data.encoding = ('utf-8')

    soup = BeautifulSoup(wb_data.text,'lxml')

    links = soup.select('div.sick_Lihide > ul > li > div > a')

    for link in links:
        page_url = link.get('href')
        print page_url + 'wait/'

    print len(links)
get_chennel_urls(start_url)
