import re
import json
import logging
import scrapy
from items import SheetItem, MusicItem, MusicianItem, UserItem


class YuzhongSpider(scrapy.Spider):
    """
    语种spider
    """
    name = 'yuzhong'
    allow_domain = 'https://music.163.com/'
    baseurl = 'https://music.163.com/discover/playlist/?cat='
    sub_names = ['华语']

    # sub_names = ['华语', '欧美', '日语', '韩语', '粤语', '小语种']

    def __init__(self):

        self.start_urls = [self.baseurl + x for x in self.sub_names]

    def parse(self, response):

        """
        爬取歌单
        :param response: 
        :return: 
        """
        sheet_urls = response.xpath('//a[starts-with(@href, "/playlist?id=")][@class="msk"]/@href').extract()
        players = response.xpath('//ul[@id="m-pl-container"]/li/div/div/span[@class="nb"]/text()').extract()

        for index, sheet_url in enumerate(sheet_urls):
            if int(players[index].replace('万', '0000')) >= self.settings.getint('SHEET_MIN_PLAYER'):
                yield scrapy.Request(url=response.urljoin(sheet_url), callback=self.parseSheet,
                                     meta={'id': re.search('\d+', sheet_url).group(0)})

        next_url = response.xpath('//a[@class="zbtn znxt"]/@href')

        if len(next_url) > 0:
            yield scrapy.Request(url=response.urljoin(next_url[0].extract()), callback=self.parse)

    def parseSheet(self, response):
        """
        解析歌单 不保存歌单评论  只保存歌曲评论
        :param response: 
        :return: 
        """
        id = response.meta['id']
        desc = response.xpath('//div[@class="m-info f-cb"]')
        musics = response.xpath("//div[@id='song-list-pre-cache']/textarea/text()")[0].extract()
        musics = json.loads(musics)
        print('歌单url = %s' % response.url)
        for music in musics:
            musicians = music.get('artists')
            musician_ids = []
            for musician in musicians:
                musician_ids.append(musician.get('id'))
                yield MusicianItem(id=musician.get('id'), name=musician.get('name'))

            music_id = music.get('id')
            album_id = music.get('album').get('id')
            music_name = music.get('name'),  # 歌曲名
            duration = music.get('duration')  # 歌曲时长

            musicItem = MusicItem()
            musicItem['id'] = music_id
            musicItem['album_id'] = album_id
            musicItem['musician_ids'] = ','.join(str(s) for s in musician_ids)
            musicItem['duration'] = duration
            musicItem['name'] = music_name

            yield musicItem
        """
        profile_url = desc.xpath('//img[@class="j-img"]/@src')[0].extract()

        name = desc.xpath('//h2[@class="f-ff2 f-brk"]/text()')[0].extract()
        user_url = desc.xpath('//div[@class="user f-cb"]/a[starts-with(@href, "/user/home?id=")]/@href')[0].extract()
        user_id = re.search('\d+', user_url).group(0)
        create_time = desc.xpath('//div[@class="user f-cb"]/span[@class="time s-fc4"]')[0].extract()
        create_time = re.search('\d{4}-\d{2}-\d{2}', create_time).group(0)
        collection_count = desc.xpath('//div[@id="content-operation"]/a[contains(@class, "u-btni-fav")]/i/text()')[0].extract()
        collection_count = re.search('\d+', collection_count).group(0)

        share_count = desc.xpath('//div[@id="content-operation"]/a[contains(@class, "u-btni-share")]/i/text()')[0].extract()
        share_count = re.search('\d+', share_count).group(0)

        comment_count = desc.xpath('//span[@id="cnt_comment_count"]/text()')[0].extract()

        player_count = response.xpath('//strong[@id="play-count"]/text()')[0].extract()
        labels = desc.xpath('//a[@class="u-tag"]/i/text()').extract()

        introduction = desc.xpath('//p[@id="album-desc-more"]')

        introduction = introduction.xpath('string(.)')[0].extract()

        sheetItem = SheetItem()
        sheetItem['id'] = id
        sheetItem['name'] = name
        sheetItem['user_id'] = user_id
        sheetItem['profile_url'] = profile_url
        sheetItem['create_time'] = create_time
        sheetItem['player_count'] = int(player_count)
        sheetItem['collection_count'] = int(collection_count)
        sheetItem['share_count'] = int(share_count)
        sheetItem['comments_count'] = int(comment_count)
        sheetItem['labels'] = labels
        sheetItem['introduction'] = introduction
        yield sheetItem

        #这里需要根据缓存判断用户是否已经保存  因为一个用户有多个歌单会重复爬取用户
        yield scrapy.Request(url=response.urljoin(user_url), callback=self.parseUser)

        """

    def parseUser(self, response):
        """
            解析用户
        """
        data = response.xpath('//div[@class="g-bd"]')

        profile_url = data.xpath('//dt[@id="ava"]/img/@src')[0].extract()

        h2 = data.xpath('//h2[@id="j-name-wrap"]')

        n = h2.xpath('./span/text()').extract()

        name = n[0]
        level = n[1]

        sex_cls = h2.xpath('./i/@class')[0].extract()

        if 'u-icn-01' in sex_cls:
            sex = 0  # 男
        elif 'u-icn-02' in sex_cls:
            sex = 1  # 女
        else:
            sex = 2  # 未知

        moment_count = data.xpath('//*[@id="event_count"]/text()')[0].extract()
        fans_count = data.xpath('//*[@id="fan_count"]/text()')[0].extract()
        follow_count = data.xpath('//*[@id="follow_count"]/text()')[0].extract()

        data.xpath('//div[@class="inf s-fc3"]/span')



