from scrapy.spider import Spider
from scrapy.selector import Selector

from metacriticbot.items import Game


class MetacriticSpider(Spider):
    name = "metacritic"
    allowed_domains = ["metacritic.com"]
    start_urls = [
            "http://www.metacritic.com/game/pc/b-17-flying-fortress-the-mighty-8th"
            #        "http://www.metacritic.com/game",
            ]


    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)

#TITLE - response.xpath('//div[@class="product_title"]/a/span[@itemprop="name"]/text()').extract()[0].strip()
