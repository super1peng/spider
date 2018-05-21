#coding:utf-8

import os
import requests
from urllib.parse import urlencode
from hashlib import md5
import time
from multiprocessing.pool import Pool

def get_page(offset):

	# https://www.toutiao.com/search_content/
	# ?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D
	# &autoload=true&count=20&cur_tab=1
	# 构造 ajax url请求
	params = {
		'offset': offset,
		'format': 'json',
		'keyword': '街拍',
		'autoload': 'true',
		'count': '20',
		'cur_tab': '3',
        'from': 'gallery',
	}

	base_url = 'https://www.toutiao.com/search_content/?'

	url = base_url + urlencode(params)
	print(url)
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.json()
	except requests.ConnectionError:
		return None

# 获取图片信息
def get_images(json):
    data = json.get('data')
    if data:
        for item in data:
            # print(item)
            image_list = item.get('image_list')
            title = item.get('title')
            # print(image_list)
            for image in image_list:
                yield {
                    'image': image.get('url'),
                    'title': title
                }

def save_image(item):
	if not os.path.exists(item.get('title')):
		os.mkdir(item.get('title'))
	try:
		local_image_url = item.get('image') # 获取到图像的url
		
		# 此url不能直接使用，需要进行转换
		new_image_url = local_image_url.replace('list','large')
		response = requests.get('http:' + new_image_url)

		# 对图片进行存储
		if response.status_code == 200:
			file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
			if not os.path.exists(file_path):
				with open(file_path, 'wb')as f:
					f.write(response.content)
			else:
				print('Already Downloaded', file_path)
	except requests.ConnectionError:
		print('Failed to save image')


def main(offset):

	json = get_page(offset)
	for item in get_images(json):
		save_image(item)

GROUP_START = 1
GROUP_END = 5


if __name__ == '__main__':

	# 开启多线程
	pool = Pool()
	groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
	print(groups)
	time.sleep(20)
	pool.map(main, groups)
	pool.close()
	pool.join()