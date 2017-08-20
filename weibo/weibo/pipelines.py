# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import codecs

class WeiboPipeline(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = base_dir + '/data/content_1.json'

        with codecs.open(filename, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(line)

        return item
