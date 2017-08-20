# -*- coding: utf-8 -*-
import scrapy
from weibo.items import WeiboItem
from scrapy.selector import Selector

class ContentSpider(scrapy.Spider):
    name = 'content'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['https://weibo.cn/wujinggoldtyphoon?page=10',]

    cookie = {
        'SUB':'_2A250nWxKDeRhGeNI4lQS9CvPyzSIHXVUfnQCrDV6PUJbktBeLUHAkW1WoS-60nN5wrs2EqeadAXlufAn7A..',
        'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFpF70GzU6OjBAXas-dcpSa5JpX5o2p5NHD95QfSo.ce0Bfe05RWs4Dqc_Ii--fiKLFi-27i--Xi-zRi-iWi--ciKnRiK.pi--ciK.Ri-8si--Xi-i2i-27i--NiKLWiKnXi--fi-z7iKysi--fi-2Xi-8Wi--4iK.Ri-z0i--fiK.fiKyW',
        'SUHB':'0FQbVKMvJkxchA',
    }


    headers = {
        "Host":"weibo.cn",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],headers=self.headers,cookies=self.cookie)

    def parse(self, response):

        items = []

        # 找到微博主的内容
        selector = Selector(response)
        infos = selector.xpath('//div[@class="c"]')

        for info in infos:
            # 先申请一个item用来保存结果信息
            item = WeiboItem()
            item['user'] = "吴京"
            item['date'] = info.xpath('div[2]/span[@class="ct"]/text()').extract()
            item['text'] = info.xpath('div/span[@class="ctt"]/text()').extract()
            item['like'] = info.xpath('div[2]/a[3]/text()').extract()
            item['transfer'] = info.xpath('div[2]/a[4]/text()').extract()
            item['comment'] = info.xpath('div[2]/a[5]/text()').extract()

            items.append(item)

        return items
