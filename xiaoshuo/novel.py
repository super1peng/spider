#coding:utf-8


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import bs4

# 抓取网页：
def get_html(url):
	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status

		#进行了手动测试编码，并设置好
		r.encoding = ('utf-8')

		return r.text

	except:
		return "Something Wrong!"

# 获取小说排行榜及其链接

def get_content(url):
	'''
	爬取每一种类型小说的排行榜，
	按照顺序写入文件，
	文件内容为：小说名字 + 小说链接
	将内容保存到列表
	并且返回一个装满url链接的列表
	'''

	url_list = [] #装满url链接的列表
	html = get_html(url)
	soup = bs4.BeautifulSoup(html, 'lxml')

	# 因为网页排版的原因，历史类和完本类小说不在一个div中

	category_list = soup.find_all('div', class_='index_toplist mright mbottom')  # 其它类

	history_finished_list = soup.find_all('div', class_='index_toplist mbottom')  # 历史类

	for cate in category_list:
		name = cate.find('div', class_='toptab').span.string
		with open('novel_list.csv','a+') as f:
			f.write("\n小说种类：{} \n".format(name))

		# 我们直接通过style属性来定位总排行榜	
		general_list = cate.find(style='display: block;')
		# 找到全部小说的名字，发现他们都包含在li标签中
		book_list = general_list.find_all('li')
		# 循环遍历出每个小说的名字，以及链接
		for book in book_list:
			link = 'http://www/qu/la' + book.a['href']
			title = book.a['title']

			# 我们将所有文章的url地址，保存在一个列表变量里
			url_list.append(link)

			# 这里使用a模式，防止清空文件
			with open('novel_list.csv', 'a') as f:
				f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))

	for cate in history_finished_list:
		name = cate.find('div', class_='toptab').span.string
		with open('novel_list.csv', 'a') as f:
			f.write("\n小说种类：{} \n".format(name))

		general_list = cate.find(style='display: block;')
		book_list = general_list.find_all('li')
		for book in book_list:
			link = 'http:/www.qu.la/' + book.a['href']
			title = book.a['title']
			url_list.append(link)
			with open('novel_list.csv', 'a') as f:
				f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))

	return url_list

#-------------获取单本小说所有章节的链接----------------
def get_text_url(url):
	'''
	获取该小说每个章节的url地址；并创建小说文件
	'''

	url_list =[]
	html = get_html(url)
	soup = bs4.BeautifulSoup(html, 'lxml')
	lista = soup.find_all('dd')
	text_name = soup.find('h1').text
	with open('/Users/lxp/Documents/Python-crawler/小说/{}.txt'.format(text.name), 'a+') as f:
		f.write('小说标题：{} \n'.format(text_name))

	for url in lista:
		url_list.append('http://www.qu.la/' + url.a['href'])

	return url_list, text_name


#-------------------获取单页文章的内容并保存到本地----------------
def get_one_text(url, text_name):
	'''
	获取小说每个章节的文本并写到本地
	'''
	html = get_html(url).replace('<br/>', '\n')
	soup = bs4.BeautifulSoup(html, 'lxml')
	try:
		text = soup.find('div', id = 'content').text.replace('chaptererror();', '')
		title = soup.find('title').text

		with open('/Users/lxp/Documents/Python-crawler/小说/{}.txt'.format(text_name), 'a') as f:
			f.write(title + '\n\n')
			f.write(text)
			print('当前小说：{} 当前章节{} 已经下载完毕'.format(text_name, title))

	except:
		print 'something wrong'



#------------------下载排行榜里所有的小说，并且保存为txt格式-----------------------
def get_all_text(url_list):
	for url in url_list:
		# 遍历获取当前小说的所有章节的目录
		# 并且生成小说的头文件
		page_list, txt_name = get_txt_url(url)
		'''
        for page_url in page_list:
            # 遍历每一篇小说，并下载到目录
            get_one_txt(page_url, txt_name)
            print('当前进度 {}% '.format(url_list.index(url) / len(url_list) * 100))
        '''



#--------------------------------END------------------------------------------


def main():
	# 排行榜地址
	base_url = 'http://www.qu.la/paihangbang/'

	# 获取排行榜中所有小说的链接
	url_list = get_content(base_url)

	# 除去重复的小说，增加效率
	#url_list = list(set(url_list))
	#get_all_text(url_list)

if __name__ == '__main__':
	main()
