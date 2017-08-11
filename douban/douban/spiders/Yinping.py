# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
from scrapy.selector import Selector

class YinpingSpider(scrapy.Spider):
	name = 'Yinping'
	start_urls = ['https://movie.douban.com/subject/26816383/comments',
				  'https://movie.douban.com/subject/26816383/comments?start=21&amp;limit=20&amp;sort=new_score&amp;status=P',
				  'https://movie.douban.com/subject/26816383/comments?start=41&amp;limit=20&amp;sort=new_score&amp;status=P',
				  'https://movie.douban.com/subject/26816383/comments?start=61&amp;limit=20&amp;sort=new_score&amp;status=P',
				  'https://movie.douban.com/subject/26816383/comments?start=81&amp;limit=20&amp;sort=new_score&amp;status=P',
				  'https://movie.douban.com/subject/26816383/comments?start=101&amp;limit=20&amp;sort=new_score&amp;status=P',
				  'https://movie.douban.com/subject/26816383/comments?start=121&amp;limit=20&amp;sort=new_score&amp;status=P',
				  'https://movie.douban.com/subject/26816383/comments?start=141&amp;limit=20&amp;sort=new_score&amp;status=P']

	def parse(self, response):

		items = []

		# 找到包含着所有用户影评信息的div

		selector = Selector(response)
		infos = selector.xpath('//div[@class="comment-item"]')
		print ("进入parse函数")
		# 筛选出每个用户的信息
		for info in infos:

			# 先申请一个DoubanItem用来保存结果:
			item = DoubanItem()
			# 观察网页，添加数据
			item['movie'] = "喜欢你"
			item['title'] = info.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').extract()
			item['num'] = info.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span//text()').extract()
			item['date'] = info.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[3]//text()').extract()
			item['score'] = info.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@title').extract()
			item['content'] = info.xpath('div[@class="comment"]/p//text()').extract()
			# 数据添加完毕

			# 将每组数据添加到总items中
			items.append(item)

		return items

		
