import scrapy

class KidsnetIndexSpider(scrapy.Spider):
    name = "kidsnet_index"

    def start_requests(self):
        urls = []
        for i in range(46):
            num = '{0:02d}'.format(i + 1)
            urls.append('https://kids.gakken.co.jp/jiten/' + num + '.html')
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
        for a in response.css('.list a'):
            item['title'] = a.css('::text').extract_first()
            link = a.css('::attr(href)').extract_first()
            item['link'] = response.urljoin(link)
            yield item
