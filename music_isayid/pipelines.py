# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class SheetPipeline(object):
    """
        歌单流水线
    """

    def __init__(self, mongo_host, mongo_db):
        """
        这里的参数就是从下面的form_crawler传进来的
        所以from_crawler必须返回pipeline实例，实质就是调用new 实例
        from_crawler函数可不写
        :param mongo_host: 
        :param mongo_db: 
        """
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host = crawler.settings.get('MONGO_HOST'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        self.db[collection_name].insert(dict(item))
        return item
