#coding:utf-8

import json
import requests


def main():
	cookies_url = 'http://0.0.0.0:5000/weibo/random'
	response = requests.get(cookies_url)
	cookies = response.text
	cookies = json.loads(cookies)
	test_url = 'https://s.weibo.com/weibo/d&scope=ori&suball=1&page=8'
	response_test = requests.get(test_url, cookies=cookies)
	print(response_test.text)

if __name__ == '__main__':
	main()