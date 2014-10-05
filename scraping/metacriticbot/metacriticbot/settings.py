# -*- coding: utf-8 -*-

# Scrapy settings for metacriticbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'metacriticbot'

SPIDER_MODULES = ['metacriticbot.spiders']
NEWSPIDER_MODULE = 'metacriticbot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'metacriticbot (+http://www.yourdomain.com)'

# Spoofing to resolve 301 redirections problem
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686; rv:24.0) Gecko/20140903 Firefox/24.0 Iceweasel/24.8.0'

#Pipelines. Some data cleaning.
ITEM_PIPELINES = {
    'metacriticbot.pipelines.MetacriticbotPipeline': 100,
}

