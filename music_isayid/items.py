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
    comment_count = scrapy.Field()#评论数
    labels = scrapy.Field()#标签
    introduction = scrapy.Field()#介绍


class MusicItem(scrapy.Item):
    """
        歌曲实体
    """
    id = scrapy.Field()#网易云音乐ID
    name = scrapy.Field()#网易云音乐名称
    musician_ids = scrapy.Field()#网易云音乐音乐人ID(s)
    duration = scrapy.Field()#网易云音乐播放时长 (毫秒)
    album_id = scrapy.Field()#网易云音乐专辑ID
    alias = scrapy.Field()#歌曲别名



class AlbumItem(scrapy.Item):
    """
        专辑实体
    """
    id = scrapy.Field()#专辑ID
    name = scrapy.Field()#专辑名称
    profile_url = scrapy.Field()#专辑图片
    musician_id = scrapy.Field()#专辑音乐人ID
    release_time = scrapy.Field()#发行时间
    release_company = scrapy.Field()#发行公司
    share_count = scrapy.Field()#分享数
    comment_count = scrapy.Field()#评论数
    introduction = scrapy.Field()#专辑介绍


class MusicianItem(scrapy.Item):
    """
        音乐人实体
    """
    id = scrapy.Field()#网易云音乐人ID
    name = scrapy.Field()#音乐人名称
    alias = scrapy.Field()#音乐人别名


class UserItem(scrapy.Item):
    """
        用户实体
    """
    id = scrapy.Field()#网易云音乐用户ID
    name = scrapy.Field()#用户名
    profile_url = scrapy.Field()#个人头像
    level = scrapy.Field()#等级
    moment_count = scrapy.Field()#动态数
    follow_count = scrapy.Field()#关注数
    fans_count = scrapy.Field()#粉丝数
    introduction = scrapy.Field()#介绍 非必须
    address = scrapy.Field()#地址
    age = scrapy.Field()#年龄 非必须
    sex = scrapy.Field()#性别 非必须 0男 1女 2未知
    #labels = scrapy.Field()#个人标签 非必须
    #type = scrapy.Field()#用户类型 1普通用户 2达人  3 V认证用户
    #created_sheet_id = scrapy.Field()#用户创建的歌单ID
    #collecting_sheet_id = scrapy.Field()#用户收藏的歌单ID
