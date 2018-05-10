import requests
import re
import time
from bs4 import BeautifulSoup

def get_one_page(url):
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
		response = requests.get(url, headers=headers, timeout=10)
		print(response.status_code)
		if response.status_code == 200:
			return response.text

		return None
	except Exception as e:
		print(e)
		return None

	return

def parse_one_page(html, info):
	info  = []
	soup = BeautifulSoup(html, 'lxml')
	content = soup.find('div',class_="mod-bd")
	# print(content)
	items = content.find_all('div',class_="comment-item")
	# print(items)
	for item in items:
		comic = {}
		a = item.find("h3")
		comic['User'] = a.find('a').text.strip()
		comic['Time'] = a.find('span',class_="comment-time ").text.strip()
		comic['Comment'] = item.find('p').text.strip()
		info.append(comic)
	return info


def main(start):
	info = {}
	url = 'https://movie.douban.com/subject/4920389/comments?start=' + str(start) + '&limit=20&sort=new_score&status=P&percent_type='
	html = get_one_page(url)
	data = parse_one_page(html, info)
	print(data)


if __name__ == '__main__':
	for i in range(10):

		main(i*20)
		print("本页采集完毕")
		time.sleep(1) # 采集完毕则停止一秒