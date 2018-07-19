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

class GooSpider(scrapy.Spider):
    name = "goo"

    def start_requests(self):
        csv_file = open('ai_index.csv')
        ai_index = csv.reader(csv_file)
        header = next(ai_index)
        urls = []
        # for ind in ai_index:
        #     ind_url = urllib.parse.quote(ind[0])
        #     urls.append('https://dictionary.goo.ne.jp/srch/all/' + ind_url + '/m1u/')
        urls.append('https://dictionary.goo.ne.jp/srch/all/%E3%82%A2%E3%83%BC%E3%82%B1%E3%83%BC%E3%83%89/m1u/')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first()

        item = {}
        item['title'] = extract_with_xpath('//div[@id="mw-content-text"]/section/div[@class="example_sentence"]/ul/li/a/p/text()')
        doc = extract_with_xpath('//div[@id="mw-content-text"]/section/div[@class="example_sentence"]/ul/li/a/@href')
        item['desc'] = MyHtmlStripper(doc).value
        yield item

