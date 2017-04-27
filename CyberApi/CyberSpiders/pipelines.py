# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymodm
from CyberSpiders import articlemodel

class CyberspidersPipeline(object):
    def open_spider(self, spider):
        pymodm.connection.connect('mongodb://jodo1991:cybernews@ds159220.mlab.com:59220/cybernewsarticles', alias='articledb')
    def process_item(self, item, spider):
        articlemodel.Article(item['id'], item['uri'], item['date'], item['author'], item['title'], item['body'],
                             item['polarity'], item['subjectivity']).save()
        return item

