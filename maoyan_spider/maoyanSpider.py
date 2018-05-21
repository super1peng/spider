#coding:utf-8

import requests
import re
import json
import time

'''
读取一个网页
'''
def get_one_page(url):
	headers = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS 10_13_3) AppleWebKit/53736 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.6'
	}

	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		return response.text
	return None


'''
用正则表达式对页面进行解析
params:
	html
'''
def parse_one_page(html):
	pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S
                         )
	items = re.findall(pattern, html)
	for item in items:
		yield {
			'index':item[0],
			'image':item[1],
			'title':item[2].strip(),
			'actor': item[3].strip()[3:],
			'time': item[4].strip()[5:],
            'score': item[5] + item[6]
		}

def write_to_file(content):
	with open('result.txt','a', encoding="utf-8") as f:
		f.write(json.dumps(content, ensure_ascii=False) + '\n')


# 传入偏置参数
def main(offset):
	url = "http://maoyan.com/board/4" + str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		write_to_file(item)


if __name__ == '__main__':
	for i in range(10):
		main(offset=i * 10)
		time.sleep(1)