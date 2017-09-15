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
    user_id = scrapy.Field()#歌单作者
    profile_url = scrapy.Field()#歌单图片url
    create_time = scrapy.Field()#创建时间
    player_count = scrapy.Field()#播放数
    collect_count = scrapy.Field()#收藏数
    share_count = scrapy.Field()#分享数
    comments_count = scrapy.Field()#评论数
    labels = scrapy.Field()#标签
    introduction = scrapy.Field()#介绍


class User(scrapy.Item):
    """
        用户实体
    """
    id = scrapy.Field()#网易云音乐用户ID
    name = scrapy.Field()#用户名
    profile_url = scrapy.Field()#个人头像
    level = scrapy.Field()#等级
    moment = scrapy.Field()#动态数
    follow = scrapy.Field()#关注数
    fans = scrapy.Field()#粉丝数
    introduction = scrapy.Field()#介绍 非必须
    address = scrapy.Field()#地址
    age = scrapy.Field()#年龄 非必须
    sex = scrapy.Field()#性别 非必须 0男 1女 2未知
    labels = scrapy.Field()#个人标签 非必须
    type = scrapy.Field()#用户类型 1普通用户 2达人  3 V认证用户
    created_sheet_id = scrapy.Field()#用户创建的歌单ID
    collecting_sheet_id = scrapy.Field()#用户收藏的歌单ID
