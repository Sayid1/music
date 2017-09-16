from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import logging
from spiders.yuzhong import YuzhongSpider

LOG_FILENAME = "log.log"

file = "runnerRes.csv" #your results
TO_CRAWL = [YuzhongSpider]

RUNNING_CRAWLERS = []

def spider_closing(spider):
    """Activates on spider closed signal"""
    logging.msg("Spider closed: %s" % spider, level=logging.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()


logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
for spider in TO_CRAWL:
    settings = Settings()
    settings.set("FEED_FORMAT", 'csv')
    settings.set("FEED_URI", file)
    settings.set("SHEET_MIN_PLAYER", 100000)
    settings.set("DOWNLOAD_DELAY", 1)
    crawler = CrawlerProcess(settings)
    crawler_obj = spider()
    RUNNING_CRAWLERS.append(crawler_obj)

    dispatcher.connect(spider_closing, signal=signals.spider_closed)
    crawler.crawl(crawler_obj)
    crawler.start()

reactor.run()