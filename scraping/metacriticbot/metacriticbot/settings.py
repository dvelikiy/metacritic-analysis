# -*- coding: utf-8 -*-

# Scrapy settings for metacriticbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
from datetime import datetime

BOT_NAME = 'metacriticbot'

SPIDER_MODULES = ['metacriticbot.spiders']
NEWSPIDER_MODULE = 'metacriticbot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'metacriticbot (+http://www.yourdomain.com)'

# Spoofing to resolve 301 redirections problem (Not really...)
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686; rv:24.0) Gecko/20140903 Firefox/24.0 Iceweasel/24.8.0'

#Pipelines. Some data cleaning. Export to xls.
ITEM_PIPELINES = {
    'metacriticbot.pipelines.MetacriticbotPipeline': 100,
    'metacriticbot.pipelines.XlsExportPipeline': 200,
}

# Feed Exports
TIMESTR = datetime.now().strftime("%Y%m%d-%H%M%S")
cur_dir = os.path.dirname(os.path.realpath(__file__))
components = cur_dir.split(os.sep)
RELPATH = str.join(os.sep, components[:components.index("metacritic-analysis")+1])

FEED_URI = os.path.join(RELPATH, 'data', '%(name)s-' + TIMESTR + '.csv')
       #os.path.join(relpath, 'data', '%(name)s-%(time)s.json')
       # ]
FEED_FORMAT = 'csv'

#Logging
logname = "log-" + TIMESTR + ".log" 
LOG_FILE = os.path.join(RELPATH, 'data', logname)


