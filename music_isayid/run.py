import redisconn
import logging
import os
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from spiders.yuzhong import YuzhongSpider
from scrapy.settings import Settings

LOG_FILENAME = "log.log"

file = "runnerRes.csv" #your results
TO_CRAWL = [YuzhongSpider]

RUNNING_CRAWLERS = []

def spider_closing(spider):
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()


logger = logging.getLogger()
logger.setLevel(logging.INFO)#log等级总开关


#创建一个handler 用于写入到文件
fh = logging.FileHandler(LOG_FILENAME, mode='w', encoding='utf-8')
fh.setLevel(logging.INFO)


#再创建一个handler 用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

#设置hanlder 输出格式
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)


#把hanlder 加入到logger里面
logger.addHandler(fh)
logger.addHandler(ch)

redisconn.connect()

HOST = 'https://music.163.com/'

# 歌单地址uri
SHEET_URI = 'playlist?id='

# 用户地址uri
USER_URI = 'user/home?id='

# 歌曲地址uri
MUSIC_URI = 'song?id='

# 歌单地址前缀
SHEET_PREFIX = '%s%s' % (HOST, SHEET_URI)

# 用户地址前缀
USER_PREFIX = '%s%s' % (HOST, USER_URI)

# 歌曲地址前缀
MUSIC_PREFIX = '%s%s' % (HOST, MUSIC_URI)

for spider in TO_CRAWL:

    settings = Settings({
        'SHEET_MIN_PLAYER': 100000,
        'LOG_LEVEL': 'INFO',
        'MONGO_HOST': 'localhost',
        'MONGO_DB': 'music163',
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'pipelines.MusicPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'middlewares.DupeUrlMiddleware': 400,
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'middlewares.UserAgentMiddleware': 401,
        },
        'BOT_NAME': 'music_isayid',
        'SPIDER_MODULES': ['spiders'],
        'NEWSPIDER_MODULE': 'music_isayid.spiders',
        'FEED_FORMAT': 'csv',
        'FEED_URI': file,
        'HOST': HOST,
        'SHEET_URI': SHEET_URI,
        'USER_URI': USER_URI,
        'MUSIC_URI': MUSIC_URI,
        'SHEET_PREFIX': SHEET_PREFIX,
        'USER_PREFIX': USER_PREFIX,
        'MUSIC_PREFIX': MUSIC_PREFIX,
    })


    crawler = CrawlerProcess(settings)
    crawler_obj = spider()
    RUNNING_CRAWLERS.append(crawler_obj)

    dispatcher.connect(spider_closing, signal=signals.spider_closed)
    crawler.crawl(crawler_obj)
    crawler.start()

reactor.run()