#coding:utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from urllib.parse import quote

KEYWORD = 'ipad'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # 禁止浏览器弹出
# 设置中文
chrome_options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"')

# SERVICE_ARGS = ['--load-images=false','--disk-cache=false']  # phantjs对缓存和图片加载的设置

# chrome 不加载图片的方式
prefs = {'profile.managed_default_content_settings.images': 2}
chrome_options.add_experimental_option('prefs',prefs)


browser = webdriver.Chrome(chrome_options=chrome_options,)

wait = WebDriverWait(browser, 10) # 设置最大加载时间，如果到了最大等到时间还是没有加载出来，则抛出异常

def index_page(page):
	print('正在爬取第', page, '页')

	try:
		url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
		print(url)
		browser.get(url)
		browser.refresh()  # 刷新方法 refresh
		if page > 1:
			input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
			submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit'))) # 获取提交按键
			input.clear() # 将输入框清空
			input.send_keys(page) # 将页码输入
			submit.click() # 点击提交输入框
		wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
	except TimeoutException:
		index_page(page)
	html = browser.page_source
	browser.quit()
	return  html

def analysis_page(html):
	doc = pq(html)
	items = doc('#mainsrp-itemlist .items .item').items()  # 这个库的选择器 使用js的选择规范
	for item in items:
		product = {
			'image': item.find('.pic .img').attr('data-src'),
			'price': item.find('.price').text(),
			'deal': item.find('.deal-cnt').text(),
			'title': item.find('.title').text(),
			'shop': item.find('.shop').text(),
			'location': item.find('.location').text()
		}
		print(product)
def main():
	html = index_page(2)
	analysis_page(html)


if __name__ == '__main__':
	main()