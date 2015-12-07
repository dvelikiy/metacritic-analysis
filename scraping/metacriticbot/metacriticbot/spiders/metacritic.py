from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from metacriticbot.items import Game

#Helper functions
def safe_extract(selector, xpath_query):
    """
    Helper function that extracts info from selector object
    using the xpath query constrains. 
    If nothing can be extracted, NA is returned.
    """
    val = selector.xpath(xpath_query).extract()
    return val[0].strip() if val else 'NA'

class MetacriticSpider(Spider):
    """
    Goal: Scrape all PC games
    1. Start with "action" genre: start_url = "http://www.metacritic.com/browse/games/genre/date/action/pc"
    2. Get links for every genre page
    3. Get links for page 1..n for genre
    4. Take "genre" field from sidebar in game list, other fields from game page itself.
    5. Go to next genre.
    6. Repeat.
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

        requests = [Request(url = URL, callback = self.parse_genre) for URL in genre_links]
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
        sel = Selector(response, type = 'html')
        game = Game()
        # General info
        game['title'] = safe_extract(sel, '//hc[@class="product_title"]/a/span[@itemprop="name"]/text()')
        game['link'] = response.url
        game['release_date'] = safe_extract(sel, '//span[@itemprop="datePublished"]/text()')
        game['developer'] = safe_extract(sel, '//li[@class="summary_detail developer"]/span[@class="data"]/text()')
        game['publisher'] = safe_extract(sel, '//li[@class="summary_detail publisher"]/span[@class="data"]/a/span/text()')
        game['platform'] = safe_extract(sel, '//span[@class="platform"]/a/span[@itemprop="device"]/text()')
        game['maturity_rating'] = safe_extract(sel, '//span[@itemprop="contentRating" and @class="data"]/text()')
        game['genre'] = response.meta['genre'] #Getting genre from original 18 genre-like sections
        game['genre_tags'] = safe_extract(sel, '//span[@itemprop="genre" and @class="data"]/text()')
        #scores
        game['metascore'] = safe_extract(sel, '//span[@itemprop="ratingValue"]/text()')
        game['critics_reviews_count'] = safe_extract(sel, '//span[@itemprop="reviewCount"]/text()')
        game['user_score'] = safe_extract(sel, '//div[@class="userscore_wrap feature_userscore"]/a/div/text()')
        game['user_reviews_count'] = safe_extract(sel, '//div[@class="userscore_wrap feature_userscore"]/div/p/span/a/text()')
        yield game
