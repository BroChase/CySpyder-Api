from bs4 import BeautifulSoup
import re
import datetime
import hashlib
import scrapy
import textblob
import textwrap
from CyberSpiders import items


class krebspider(scrapy.Spider):
    name = 'krebs'
    allow_domains = ['krebsonsecurity.com']
    start_urls = ['https://krebsonsecurity.com/page/1/', ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        for href in soup.find_all('a', href=True, rel='bookmark'):
            search_page = href['href']
            self.sp = search_page
            if search_page is not None:
                yield scrapy.Request(search_page, callback=self.articleparse)

        next_page = response.css('div.navigation a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def articleparse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        titles = ""
        for title in soup.select('h2.post-title'):
            titles += title.string

        para = ""
        for paragraph in soup.select("div.entry > p"):
            if paragraph.has_attr("class") and paragraph['class'][0] == "mid-banner":
                break

            newpara = paragraph.text.strip()
            if newpara != '':
                para += '\n'.join(textwrap.wrap(newpara, width=100)) + '\n\n'

        date = ""
        for small in soup.find_all('p', 'postmetadata alt'):
            date += small.text

        n = re.search('(?P<day>\d+)', date)
        q = re.search('(?P<year>\d{4})', date)
        p = re.search('(?P<month>(, )\S+)', date)
        p = str(p.group('month'))
        p = p.replace(',', '').replace(' ', '')
        months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,
                  'August':8,'September':9,'October':10,'November':11,'December':12}

        date = datetime.datetime(int(q.group('year')), months[p], int(n.group('day')))

        item = items.CyberspidersItem()
        utf_string = response.url.encode('utf-8') + titles.encode('utf-8')
        item['id'] = hashlib.md5(utf_string).hexdigest()
        item['uri'] = response.url
        item['date'] = date
        item['author'] = "Brian Krebs"
        item['title'] = titles
        item['body'] = para
        sentiment = textblob.TextBlob(item['body'])
        item['polarity'] = sentiment.polarity
        item['subjectivity'] = sentiment.subjectivity
        yield item
