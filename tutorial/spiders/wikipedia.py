import scrapy
import csv
import io
from html.parser import HTMLParser
import urllib.parse

class MyHtmlStripper(HTMLParser):
    def __init__(self, s):
        super().__init__()
        self.sio = io.StringIO()
        self.feed(s)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        self.sio.write(data)

    @property
    def value(self):
        return self.sio.getvalue()

class WikiSpider(scrapy.Spider):
    name = "wikipedia"

    def start_requests(self):
        csv_file = open('ai_index.csv')
        ai_index = csv.reader(csv_file)
        header = next(ai_index)
        urls = []
        for ind in ai_index:
            ind_url = urllib.parse.quote(ind[0])
            urls.append('https://ja.wikipedia.org/wiki/' + ind_url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first()

        item = {}
        item['title'] = extract_with_xpath('//h1/text()')
        doc = extract_with_xpath('//div[@id="mw-content-text"]/div/p')
        item['desc'] = MyHtmlStripper(doc).value
        yield item

