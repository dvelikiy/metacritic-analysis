# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Game(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # General info
    title = scrapy.Field()
    link = scrapy.Field()
    release_date = scrapy.Field()
    publisher = scrapy.Field()
    platform = scrapy.Field()
    maturity_rating = scrapy.Field()
    genre = scrapy.Field()
    #scores
    metascore = scrapy.Field()
    critics_reviews_count = scrapy.Field()
    user_score = scrapy.Field()
    user_reviews_count = scrapy.Field()



