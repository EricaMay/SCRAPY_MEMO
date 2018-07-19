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


class YahooAstroFoodSpider(scrapy.Spider):
    name = "yahoo_astro_food"

    def start_requests(self):
        csv_file = open('y_ast_foo_index.csv')
        ai_index = csv.reader(csv_file)
        urls = []
        for ind in ai_index:
            urls.append(ind[0])
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('dt>a::attr(href)').extract():
            yield scrapy.Request(url= href, callback=self.parse_doc)

        next_page = response.css('a.link_next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_doc(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first()

        item = {}
        item['title'] = extract_with_xpath('//h1/text()')
        doc = extract_with_xpath('//p[@class="cont"]')
        trim_doc = MyHtmlStripper(doc).value
        item['doc'] = trim_doc
        yield item
