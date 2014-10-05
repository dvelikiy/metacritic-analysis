# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

class MetacriticbotPipeline(object):
    def process_item(self, item, spider):
        #so that userscore resembles metascore 0..100 scale
        #some non-numeric values such as 'tbd' are left out 
        #for the sake of uniformity
        try:
            item['user_score'] = int(float(item['user_score'])*10)
        except ValueError:
            item['user_score'] = 'NA'
        #convert to Year-month-day format
        if item['release_date'] != 'NA':
            item['release_date'] = datetime.strptime(item['release_date'], '%b %d, %Y').strftime('%Y-%m-%d')
        #leave only N out of "N Ratings" for user ratings
        item['user_reviews_count'] = item['user_reviews_count'].split()[0]
        return item
