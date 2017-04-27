import scrapy
from bs4 import BeautifulSoup
import textwrap
import re
import datetime
from CyberSpiders import items
import hashlib
import textblob


class DarkReadingSpider(scrapy.Spider):
    name = 'darkreading'
    start_urls = [
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=658',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=644',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=645',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=656',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=647',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=648',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=1217',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=651',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=655',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=652',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=653',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=659',
        'http://www.darkreading.com/archives.asp?newsandcommentary=yes&tag_id=661',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        # story...get all info
        if soup.find(id='article-main'):
            article = items.CyberspidersItem()
            article['uri'] = response.url
            authorBlock = soup.find('div', 'author-info-block')
            if authorBlock.find('span','smaller blue') is not None:
                article['author'] = authorBlock.find('span','smaller blue').a.get_text()
            else:
                article['author'] = authorBlock.find('span', 'smaller black').get_text()
            m = re.search('(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d{4})',
                          soup.find(id='thedoctop').find('span', 'smaller gray').get_text())
            article['date'] = datetime.datetime(int(m.group('year')), int(m.group('month')), int(m.group('day')))
            article['title'] = soup.find(id='article-main').header.get_text()
            utf = response.url.encode('utf-8') + article['title'].encode('utf-8')
            article['id'] = hashlib.md5(utf).hexdigest()
            article['body'] = ''
            for par in soup.find(id='article-main').find_all('p'):
                if not re.match('Related Content', par.get_text()):
                    article['body'] += '\n'.join(textwrap.wrap(par.get_text(), width=100))
                    article['body'] += '\n\n'
            article['body'] = re.sub('\\n{2,}', '\n\n', article['body'])
            sentiment = textblob.TextBlob(article['body'])
            article['polarity'] = sentiment.polarity
            article['subjectivity'] = sentiment.subjectivity
            yield article

        # if not story, find links
        # todo figure out slideshow formatting
        if soup.find('span', 'blue strong allcaps'):
            try:
                column = soup.find('div', 'column left-main')
                for tag in column.find_all('span', 'blue strong medium'):
                    if '/v/' not in tag.a['href']:
                        yield scrapy.Request(response.urljoin(tag.a['href']), callback=self.parse)
                if '&piddl_archivepage=2' not in response.url:
                    yield scrapy.Request(response.url + '&piddl_archivepage=2', callback=self.parse)
            except TypeError:
                print("ATTRIBUTE ERROR")
            except NameError:
                print("OTHER EXCEPTION")
