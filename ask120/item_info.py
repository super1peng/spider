#coding:utf-8

__author__ = 'LiXiaoPeng'
from bs4 import BeautifulSoup
import requests
import random
import time
import csv
# 导入正则表达式包
import re
# python与数据库相连接
import pymysql

import sys

# ID00 = 360634

# User-Agent
headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]

# # Proxy
# proxy_list = [
#         'http://61.153.67.110:9999',
#         'http://121.40.199.105:80',
#         'http://120.24.208.42:9999',
#         'http://120.25.211.80:9999',
#     ]
# proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
# proxies = {'http': proxy_ip}

# 读取csv文件数据
def loadfile():
    csv_reader = csv.reader(open('/Users/lxp/Desktop/first_over.csv'))
    for id, url in csv_reader:
        yield url

fileor = loadfile() # 创建一个生成器

def get_item_info():
    for url in fileor:
        #print('haha')
        # -------------数据ID00------------
        wangye_1 = url.split('/')
        wangye_2 = wangye_1[-1].split('.')
        ID00 = wangye_2[0]

        wb_data = requests.get(url, headers=random.choice(headers_pool))
        soup = BeautifulSoup(wb_data.text, 'lxml')
        try:
            # ------------科室分类--------------------
            # print('1')
            FenLei = soup.find('div',class_='b_route')
            t = FenLei.find_all('a')
            # print(t)
            YJFL = t[1].get_text()        # 一级分类
            EJFL = t[2].get_text()        # 二级分类
            SJFL = ''
            if len(t)>=4:
                SJFL = t[3].get_text()    # 三级分类
            #print(YJFL)
            #print(EJFL)
            #print(SJFL)

            # ---------------标题 发布时间 提问者年龄、性别---------------------
            # print('2')
            title = soup.find('div', class_='b_askti')
            text = title.get_text()
            a = text.split('\n')
            # print(a, len(a))
            try:
                if len(a) == 7:
                    BT00 = a[1]    # 标题
                    b = a[3].split(' ')
                    FBSJ00 = b[3]  # 发表时间
                    TWZNL = b[2][:-1]   # 提问者年龄
                    TWZXB = b[0]   # 提问者性别
                    #print(BT00)
                    #print(FBSJ00)
                    #print(TWZNL)
                    #print(TWZXB)
                elif len(a) == 8:
                    BT00 = a[1]    # 标题
                    FBSJ00 = a[4][:10]  #发表时间
                    b = a[3].split(' ')
                    #TWZNL = re.findall(r'\d+', b[2])
                    TWZNL = b[2][:-1]   # 提问者年龄
                    TWZXB = b[0]    # 提问者性别

                elif len(a) == 9:
                    BT00 = a[1]   # 标题
                    FBSJ00 = a[5][:10]  # 发表时间
                    b = a[3].split(' ')
                    TWZNL = b[2][:-1]  # 提问者年龄
                    TWZXB = b[0]  # 提问者性别
                else:
                    BT00 = ''
                    FBSJ00 = ''
                    TWZNL = ''
                    TWZXB = ''
            except Exception as e:
                BT00 = ''
                FBSJ00 = ''
                TWZNL = ''
                TWZXB = ''

            # ----------疾病问题描述------------
            # print('3')
            jibing_1 = soup.find('div', class_='b_askcont')
            jibing_2 = jibing_1.find('p', class_='crazy_new')
            miaoshu = jibing_2.get_text()
            miaoshu_1 = miaoshu.split(' ')
            WT00 = miaoshu_1[20]   # 疾病问题描述
            #print(WT00)

            # ---------对医生列表的提取----------
            # 首先判断有多少个医生进行了回答
            # print('4')
            yisheng = soup.find_all('div', class_='b_answerli')
            # 医生数等于 len(yisheng)-1
            # print(len(yisheng))
            for i in range(len(yisheng)):
                t = yisheng[i]
                shanchang = t.find('span', 'b_sp2')
                if shanchang == None:
                    continue
                zhiwei = t.find('span', class_='b_sp1').get_text()
                try:
                    c = zhiwei.split(' ')
                    HDZZW = c[2]     # 回答者职位
                except Exception as e:
                    HDZZW = ''

                #print(HDZZW)
                try:
                    HDZSC = shanchang.get_text() # 回答者擅长
                except Exception as e:
                    HDZSC = ''
                #print(HDZSC)
                try:
                    HDZBZSM = t.find('em').get_text()  # 回答者帮助数目
                except Exception as e:
                    HDZBZSM = ''
                #print(HDZBZSM)
                try:
                    time = t.find('span',class_='b_anscont_time')
                    time_text = time.get_text()
                    tt = time_text.split('\t')[1]
                    HDSJ00 = tt[:10]    # 回答时间
                except Exception as e:
                    HDSJ00 = ''
                #print(HDSJ00)

                result = t.find('div', class_='crazy_new')
                try:
                    con = result.get_text()
                    HDNN = con[7:]      # 回答内容
                except Exception as e:
                    HDNN = ''
                #print(HDNN)

                #--------------医生意见是否被采纳-------------------
                caina = t.find('i',class_='b_acceptico')
                if caina != None:
                    SFCN00 = 1   # 1:被采纳
                else:
                    SFCN00 = 0  # 0:未被采纳
                #print(SFCN00)

                # print('5')

                # 将数据导入数据库:数据库名称(spider),表名(result_test)
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123lxp', db='spider',use_unicode=True,charset='utf8')
                cur = conn.cursor()
                # conn.set_character_set('utf8')
                # cur.execute('SET NAMES utf8;')
                # cur.execute('SET CHARACTER SET utf8;')
                # cur.execute('SET character_set_connection=utf8;')
                # cur.execute('insert into result_test values (%s)',[str(ID00)])
                cur.execute("INSERT INTO result_1 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[ID00,YJFL,EJFL,SJFL,BT00,FBSJ00,WT00,TWZNL,TWZXB,HDZZW,HDZSC,HDZBZSM,HDSJ00,SFCN00,HDNN])
                conn.commit()
                cur.close()
                conn.close()

                #print("-------------------医生分割线---------------")

            print(url)
        except Exception as e:
            continue
        print("------------------下个网页-----------------")


if __name__ == '__main__':
    print(sys.stdout.encoding)
    get_item_info()