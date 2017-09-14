# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SheetItem(scrapy.Item):
    """
        歌单实体 歌单url = SHEET_PREFIX + id
    """
    id = scrapy.Field()#网易云歌单ID
    name = scrapy.Field()#歌单名称
    author = scrapy.Field()#歌单作者
    profile_url = scrapy.Field()#歌单图片url
    create_time = scrapy.Field()#创建时间
    player_count = scrapy.Field()#播放数
    collection_count = scrapy.Field()#收藏数
    share_count = scrapy.Field()#分享数
    comments_count = scrapy.Field()#评论数
    labels = scrapy.Field()#标签
    introduction = scrapy.Field()#介绍


