from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from metacriticbot.items import Game


class MetacriticSpider(Spider):
    """
    Goal: Scrape all PC games
    0. Probably create dictionary that maps short genre names with long genre names.
    1. Start with "action" genre: start_url = "http://www.metacritic.com/browse/games/genre/date/action/pc"
    2. Get links for every genre page
    3. Get links for page 1..n for genre
    4. Need variable to store genre name
    5. Take "genre" field from sidebar in game list, other fields from game page itself.
    6. Go to next genre.
    7. Repeat.
    """
    name = "metacritic"
    allowed_domains = ["metacritic.com"]
    start_urls = [
            "http://www.metacritic.com/browse/games/genre/date/action/pc?view=detailed"
            ]


    #Get genre list from start_url, generate requests to parse genre pages later
    def parse(self, response):
        genres = [s.split()[1].split('_', 1)[1].replace("_", "-") for s in response.xpath('//ul[@class="genre_nav"]/li/@class').extract()]
        genre_links = ["http://www.metacritic.com/browse/games/genre/date/" + genre + "/pc" for genre in genres]

        #requests = [Request(url = URL, callback = self.parse_genre) for URL in genre_links]
        self.log("###INITIAL PARSING ### " + str(len(genre_links)) + " Genres IN THIS TOTAL LIST")
        return requests

    #Get all pages for a genre, send them to page parser
    def parse_genre(self, response):
        try:
            page_links = [response.url + "?page=" + str(i) for i in range(int(response.xpath('//li[@class="page last_page"]/a/text()').extract()[0]))]
        except IndexError:
            page_links = [response.url]

        requests = [Request(url = URL, callback = self.parse_page) for URL in page_links]
        self.log("###PARSING GENRE### " + str(len(page_links)) + " PAGES IN THIS GENRE")
        return requests

    #Get all games for a page
    def parse_page(self, response):
        game_links = ["http://metacritic.com" + postfix for postfix in response.xpath('//ol[@class="list_products list_product_condensed"]/li/div/div/a/@href').extract()]
        meta_genre = response.xpath('//div[@class="module products_module list_product_condensed_module "]/div/div/h2[@class="module_title"]/text()').extract()[0].strip()
        requests = [Request(url = URL, callback = self.parse_game, meta = {'genre': meta_genre}) for URL in game_links]
        self.log("###PARSING PAGE### " + str(len(game_links)) + " GAMES IN THIS PAGE")
        return requests

    def parse_game(self, response):
        game = Game()
        # General info
        game['title'] = response.xpath('//div[@class="product_title"]/a/span[@itemprop="name"]/text()').extract()[0].strip()
        game['link'] = response.url
        game['release_date'] = response.xpath('//span[@itemprop="datePublished"]/text()').extract()[0].strip()
        game['publisher'] = response.xpath('//li[@class="summary_detail developer"]/span[@class="data"]/text()').extract()[0].strip()
        game['platform'] = response.xpath('//span[@class="platform"]/a/span[@itemprop="device"]/text()').extract()[0].strip()
        #maturity_rating = scrapy.Field()
        game['genre'] = response.meta['genre'] 
        #scores
        game['metascore'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0].strip()
        game['critics_reviews_count'] = response.xpath('//span[@itemprop="reviewCount"]/text()').extract()[0].strip()
        game['user_score'] = response.xpath('//div[@class="userscore_wrap feature_userscore"]/a/div/text()').extract()[0].strip()
        game['user_reviews_count'] = response.xpath('//div[@class="userscore_wrap feature_userscore"]/div/p/span/a/text()').extract()[0].strip()
