import io
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


class YahooSpider(scrapy.Spider):
    name = "yahoo"

    def start_requests(self):
        for i in range(1):
            num = '{0:02d}'.format(i + 1)
            urls = [
                'https://kids.gakken.co.jp/jiten/' + num + '.html',
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('.list a::attr(href)').extract():
            href = response.urljoin(href)
            yield scrapy.Request(url= href, callback=self.parse_doc)

    def parse_doc(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first()

        item = {}
        item['title'] = extract_with_xpath('//article/h1/text()')
        doc = extract_with_xpath('//article/p[position()=1]')
        trim_doc = MyHtmlStripper(doc).value
        item['doc'] = trim_doc
        yield item
