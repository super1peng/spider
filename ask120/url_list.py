#coding:utf-8

__author__ = 'LiXiaoPeng'

# spider1 爬取有问必答按科室分类后的问题列表中的url

from bs4 import BeautifulSoup
import requests
import random
import time
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# User-Agent
headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]


id = 1

def get_url_list(channel, page):
    # 网页url例子:http://www.120ask.com/list/gdjbwk/wait/2/
    # python-mysql
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123lxp',
        db='spider',
    )
    cur = conn.cursor()
    global id
    list_view = '{}{}/'.format(channel, str(page))
    print list_view
    wb_data = requests.get(list_view, timeout=30, headers=random.choice(headers_pool))

    soup = BeautifulSoup(wb_data.text, 'lxml')
    urls = soup.find_all('a',attrs={'class':'q-quename'})

    for url in urls:
        cur.execute("INSERT INTO url_list2 VALUES (%s, %s)", [str(id), url.get('href')])
        id = id + 1

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    file = open('/Users/lxp/Desktop/page_url_over.txt','r')
    for line in file.readlines():
        for page in range(1,201):
            get_url_list(line[:-1], page)