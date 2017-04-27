# import scrapy
# from bs4 import BeautifulSoup
# import textwrap
# import re
# import datetime
# from CyberSpiders import items
#
#
# class Spider(scrapy.Spider):
#     name = ''
#     start_urls = []
#
#     def parse(self, response):
#         soup = BeautifulSoup(response.body, 'lxml')
#
#         article = items.CyberspidersItem()
#
#         yield article
#
#         yield scrapy.Request(, callback=self.parse)

