import scrapy
from bs4 import BeautifulSoup
import textwrap
import hashlib
import textblob
from CyberSpiders import items
from time import time

limit = 10
class Threatpost(scrapy.Spider):
    name = 'threatpost'
    start_urls = [
        'https://threatpost.com/blog/',
        'https://threatpost.com/blog/page/2/'
    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 1
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        #get article links to parse
        for article_tag in soup.find(id='latest-posts').find_all("article"):
            yield scrapy.Request(article_tag.div.a['href'], callback=self.articleparse)

        #initial page, handle seperately
        if '/page/' not in response.url:
            for page in range(2, limit):
                yield scrapy.Request(response.url+'page/{}/'.format(page), callback=self.parse)

    def articleparse(self, response):
        temp = time()
        main_article = BeautifulSoup(response.body, 'lxml').find(id='content').article
        header = main_article.header
        body = main_article.find(itemprop="articleBody")

        article = items.CyberspidersItem()
        article['uri'] = response.url
        article['date'] = header.find('time')['datetime']
        article['author'] = header.find(itemprop="author").a.get_text()
        article['title'] = header.div.h1.get_text()
        article['body'] = ""
        for paragraph in body.find_all('p'):
            article['body'] += '\n'.join(textwrap.wrap(paragraph.get_text(),width=100))+' \n\n'
        article['id'] = hashlib.md5(article['uri'].encode('utf-8')+article['title'].encode('utf-8')).hexdigest()

        sentiment = textblob.TextBlob(article['body'])
        article['polarity'] = sentiment.polarity
        article['subjectivity'] = sentiment.subjectivity
        yield article