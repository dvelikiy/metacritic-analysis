from scrapy.spider import Spider
from scrapy.selector import Selector

from metacriticbot.items import Game


class MetacriticSpider(Spider):
    name = "metacritic"
    allowed_domains = ["metacritic.com"]
    start_urls = [
        "http://www.metacritic.com/game",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        ...

        """
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s([^\n]*?)\\n')
            items.append(item)

        return items
