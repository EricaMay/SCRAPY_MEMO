import io
import csv
from html.parser import HTMLParser
import scrapy

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


class KidsnetSpider(scrapy.Spider):
    name = "kidsnet"

    def start_requests(self):
        csv_file = open('kidsnet_index.csv')
        ai_index = csv.reader(csv_file)
        urls = []
        for ind in ai_index:
            urls.append(ind[0])
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first()

        item = {}
        item['title'] = extract_with_xpath('//h1/text()')
        doc = extract_with_xpath('//article/p[position()=1]')
        trim_doc = MyHtmlStripper(doc).value
        item['doc'] = trim_doc
        yield item