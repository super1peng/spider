from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pymysql
import re

def test(typhon_name,url):
	driver = webdriver.Chrome()
	driver.get(url)
	# driver.get('https://m.weibo.cn/p/100808dedc522b783370e6e336115f8f438f2d')
	time.sleep(10) # 延迟10 让页面进行加载

	# 在此进行页面加载
	for k in range(20):
		#将页面滚动条拖到底部
		time.sleep(5)
		try:
			js="var q=document.documentElement.scrollTop=1000000"  
			driver.execute_script(js)
		except:
			continue
	print("页面加载完毕")

	co = re.compile(u'[\U00010000-\U0010ffff]') # 去掉表情符号

	# print(driver.page_source)
	# content = driver.find_element_by_class_name("WB_frame_c")
	data = driver.page_source
	soup = BeautifulSoup(data,'lxml')
	count = 0 # 统计数据数目
	contents = soup.find_all('div',class_='card card11 ctype-2')
	# print(len(contents))
	for i in contents:
		hh = i.find('div', class_='card-list')
		# info = hh.find_all('card m-panel card9')
		# print(len(info))
		for j in hh.children:
			try:
				header = j.find('header',class_='weibo-top m-box m-avatar-box')
				name = j.find('h3',class_='m-text-cut').text.replace(' ','').replace('\n','')
				name = co.sub(u'',name)
				print("name",name)
				timestrap = j.find('h4',class_='m-text-cut').find('span').text.replace('\n','')
				# e = timestrap.split()
				# timestrap = e[0] + " " + e[1]
				print("time",timestrap)
				article = j.find('article',class_='weibo-main')
				neirong = article.find('div',class_='weibo-text').text
				neirong = co.sub(u'',neirong)
				neirong = neirong.replace(' ','').replace('\n','').replace('"',' ')
				# print("name",name)
				# print("time",timestrap)
				print("neirong",neirong)
			except:
				continue
			# 将数据存储进mysql
			# 建立数据库连接
			conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123lxp',db='Storyline',charset='utf8')
			cursor = conn.cursor()
			cursor.execute('INSERT INTO weibo(typhon_name, \
			         nickname, information, timestrap) \
			         VALUES ("%s","%s","%s","%s")' % (typhon_name,name, neirong, timestrap))
			conn.commit()
			conn.close()
			count = count + 1
	driver.close()
	print(count)
if __name__ == "__main__":
	typhon_names = ["梅花","苗柏","南玛都","塔拉斯","奥鹿","玫瑰","洛克","桑卡","纳沙","海棠","尼格","榕树","天鸽","帕卡","珊瑚",\
			"玛娃","古超","泰利","杜苏芮","卡努","兰恩","苏拉","达维","海葵","鸿雁","启德","天秤","布拉万","三巴","杰拉华"
		]
	urls = [
		"https://m.weibo.cn/p/100808dedc522b783370e6e336115f8f438f2d",
		"https://m.weibo.cn/p/100808e27c4b86eec8439d80c558a4eb8d9220",
		"https://m.weibo.cn/p/100808b7eb992b88fa57c7aeffeed7de92b89d",
		"https://m.weibo.cn/p/100808eea1517b811e74d69f5e1f9bb1a23b01",
		"https://m.weibo.cn/p/100808b5293542b0d2890c444d5ea51fdd76f5",
		"https://m.weibo.cn/p/1008087a59326a2568a8530d7c9cb7a2e0e3a6",
		"https://m.weibo.cn/p/100808d1f2091a04d5140f2f332abcea1ff380",
		"https://m.weibo.cn/p/100808ca0f63cdbd4d4b8d1b18c62ead552c3c",
		"https://m.weibo.cn/p/1008081de7ba8247d1520f82748770c6c226db",
		"https://m.weibo.cn/p/1008089eb0dc85dcadd358ecb1ed80b8bfd178",
		"https://m.weibo.cn/p/100808d860c1e6b71a2c839a2aded382784d22",
		"https://m.weibo.cn/p/1008089b927381a2d9ffa852f10416b1334a32",
		"https://m.weibo.cn/p/100808d1571baea7d86bc77ba155cd917269ba",
		"https://m.weibo.cn/p/1008086379bc88dfb4b37fa7d15c3332f149fb",
		"https://m.weibo.cn/p/1008082885651c536566fa1c7e13c95c8e824c",
		"https://m.weibo.cn/p/10080863a7743dbf022b2000561afc08148ae0",
		"https://m.weibo.cn/p/1008084aadc4de161dcb047f8c69dc27c7bdd0",
		"https://m.weibo.cn/p/100808b369d0cb9ad5be9d0ebc320ae089e3e7",
		"https://m.weibo.cn/p/100808c500d4c45a8277bc039d850e268568a9",
		"https://m.weibo.cn/p/100808309a761b2ec62b6891574d8724e019af",
		"https://m.weibo.cn/p/10080804dfa62f4ab579a7bea8cb42cf70c2d4",
		"https://m.weibo.cn/p/10080863348730c8a31eb7693a37da52669964",
		"https://m.weibo.cn/p/100808485b067938a6de31ff139316a0e3b17a",
		"https://m.weibo.cn/p/1008081838b9f823ac71053bcebb51c6aa8117",
		"https://m.weibo.cn/p/1008083e1755c71bf0f9218e6604e2b2621beb",
		"https://m.weibo.cn/p/10080805bb9ac9c56a9c6a0600bb9daab02e2a",
		"https://m.weibo.cn/p/100808e5ff003aefee908cc76979c92d0444db",
		"https://m.weibo.cn/p/1008085edb183b2c4a3c57aa9b551f1800948f",
		"https://m.weibo.cn/p/100808e05d45833e01121f2a0f1c110ac2f232",
		"https://m.weibo.cn/p/10080826801f2f8ae6ae6fa9a3c3060d875c4c",
	]
	for i in range(len(urls)):
		# print(typhon_names[i],urls[i])
		test(typhon_names[i],urls[i])
		# break