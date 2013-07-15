from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import open_in_browser
from scrapy.http import Request

from amazon.items import AmazonItem

class SampleSpider(BaseSpider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    count = 1
    rank = 0
    aboveTheFold = 1
    start_url = "http://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_electronics_pg_1?_encoding=UTF8&pg={0}&ajax=1&isAboveTheFold={1}"
    start_urls = [
        start_url.format(count, aboveTheFold)
    ]
    items = []

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        #from scrapy.shell import inspect_response
        #inspect_response(response)
        products = hxs.select('/html/body/div[@class="zg_itemImmersion"]')

        for product in products:
            self.rank += 1
            yield self.parse_details(product)

        if self.count < 6:

            if self.aboveTheFold == 1:
                self.aboveTheFold = 0
            else:
                self.aboveTheFold = 1
                self.count += 1

            yield Request(self.start_url.format(self.count, self.aboveTheFold), callback = self.parse)

        return


    def parse_details(self, profile):
        item = AmazonItem()
        item['rank'] = self.rank
        item['url'] = profile.select("div/div/a/@href").extract()[0].replace('\n','')
        item['name'] = profile.select("div/div/a/text()").extract()
        item['image'] = profile.select("div/div/div/a/img/@src").extract()
        item['price'] = profile.select("div/div/div[@class='zg_price']/strong/text()").extract()
        #item['price'] = profile.select("table/tr/td/div[2]/div[1]/span[1]/text()").extract()

        return item

#/html/body/div[2]/div[2]/div[5]/div[1]/strong