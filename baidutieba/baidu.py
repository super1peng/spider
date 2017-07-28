#coding:utf-8
'''
抓取百度贴吧------生活大爆炸的基本内容
爬虫路线：requesets --bs4
Python版本：2.7
OS: mac os

'''

import requests
import time 
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 首先我们写好抓取网页的函数

def get_html(url):
	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status()

		#我们知道百度贴吧的编码是utf-8，所以手动设置。
		#爬去其他页面时建议使用：r.endcoding = r.apparent_endconding

		r.encoding = 'utf-8'
		return r.text

	except:
		return "ERROR"

def get_content(url):

	# 初始化一个列表保存所有的帖子信息:
	comments = []

	# 首先，我们把需要爬取的信息下载到本地
	html = get_html(url)

	# 我们来做一锅汤
	soup = BeautifulSoup(html, 'lxml')

	# 按照之前的分析，我们找到所有具有 'j_thread_list clearfix'属性的li标签，返回一个列表类型
	liTags = soup.find_all('li',attrs={'class':' j_thread_list clearfix'})

	# 通过循环找到每个帖子里我们需要的信息:
	for li in liTags:
		#初始化一个字典用来存储文章信息
		comment = {}

		# 这里使用一个try except 防止爬虫找不到信息从而停止运行
		try:
			# 开始筛选信息，并保存到字典中
			comment['title'] = li.find(
				'a',attrs={'class': 'j_th_tit'}).text.strip()
			comment['link'] = "http://tieba.baidu.com/" + \
				li.find('a',attrs={'class': 'j_th_tit '})['href']
			comment['name'] = li.find(
				'span', attrs={'class':'tb_icon_author '}).text.strip()
			comment['time'] = li.find(
				'span', attrs={'class':'pull-right is_show_create_time'}).text.strip()
			comment['replyNum'] = li.find(
				'span', attrs={'class':'threadlist_rep_num center_text'}).text.strip()
			comments.append(comment)
		except:
			
			print ('出了问题!')

	return comments
	

def Out2File(dict):
	'''
	将爬取到的文件写入本地，保存到当前目录的 TTBT.txt 文件中
	'''
	with open('TTBT.txt', 'w+') as f:
		for comment in dict:
			f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))

		print('当前页面爬取完成')

def main(base_url, deep):
	url_list = []
	#将所有需要爬取的url存入列表

	for i in range(0, deep):
		url_list.append(base_url + '&pn=' +str(50 * i))
	print('所有的网页已经下载到本地！ 开始筛选信息。。。')

	# 循环写入所有的数据
	for url in url_list:
		content = get_content(url)
		Out2File(content)
	print('所有的信息都已经保存完毕！')


base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
# 设置需要爬取的页码数量
deep = 3

if __name__=='__main__':
	main(base_url, deep)
