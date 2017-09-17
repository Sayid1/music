import re
import time
import json
import logging
import scrapy
from redisconn import setMusic
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
                print(re.search('\d+', sheet_url))
                yield scrapy.Request(url=response.urljoin(sheet_url), callback=self.parseSheet, meta={'id': re.search('\d+', sheet_url).group(0)})
        """
        next_url = response.xpath('//a[@class="zbtn znxt"]/@href')

        if len(next_url) > 0:
            yield scrapy.Request(url=response.urljoin(next_url[0].extract()), callback=self.parse)
        """

    def parseSheet(self, response):
        """
        解析歌单 不保存歌单评论  只保存歌曲评论
        :param response: 
        :return: 
        """
        id = response.meta['id']
        desc = response.xpath('//div[@class="m-info f-cb"]')

        # --------------保存歌单歌曲------------------
        musics_raw = response.xpath("//div[@id='song-list-pre-cache']/textarea")[0].extract()
        #部分歌单会有奇怪现象 /text()获取的不是全部 所以采用正则表达式提取
        result = re.search(r'\[.*\]', musics_raw)

        #如果该歌单有歌曲
        if result:
            musics = result.group(0)
            musics = json.loads(musics)

            for music in musics:
                musicians = music.get('artists')
                musician_ids = []
                for musician in musicians:
                    musician_ids.append(musician.get('id'))
                    yield MusicianItem(id=musician.get('id'), name=musician.get('name'), alias=musician.get('alias'))

                music_id = music.get('id')
                album_id = music.get('album').get('id')
                music_name = music.get('name'),  # 歌曲名
                duration = music.get('duration')  # 歌曲时长
                alias = music.get('alias')#歌曲别名 eg:电视剧xxx主题曲/原唱：刘若英

                if setMusic(music_name, musician_ids):
                    musicItem = MusicItem()
                    musicItem['id'] = music_id
                    musicItem['album_id'] = album_id
                    musicItem['musician_ids'] = ','.join(str(s) for s in musician_ids)
                    musicItem['duration'] = duration
                    musicItem['name'] = music_name
                    musicItem['alias'] = alias

                    yield musicItem
                #一首歌可能存在于多个歌单中，但它们的ID是一样的，中间件会自动过滤 所以这里不需要redis去重 （评论和歌曲挂钩  不和歌单挂钩）
                yield scrapy.Request(url='%s%s' % (self.settings.get('MUSIC_PREFIX'), music_id), callback=self.parseMusic)
        #----------------歌曲end-----------------

        #----------------歌单信息----------------
        profile_url = desc.xpath('//img[@class="j-img"]/@src')[0].extract()

        name = desc.xpath('//h2[@class="f-ff2 f-brk"]/text()')[0].extract()
        user_url = desc.xpath('//div[@class="user f-cb"]/a[starts-with(@href, "/user/home?id=")]/@href')[0].extract()
        user_id = re.search('\d+', user_url).group(0)
        create_time = desc.xpath('//div[@class="user f-cb"]/span[@class="time s-fc4"]')[0].extract()
        create_time = re.search('\d{4}-\d{2}-\d{2}', create_time).group(0)
        collect_count = desc.xpath('//div[@id="content-operation"]/a[contains(@class, "u-btni-fav")]/i/text()')[0].extract()
        collect_count = re.search('\d+', collect_count).group(0)

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
        sheetItem['collect_count'] = int(collect_count)
        sheetItem['share_count'] = int(share_count)
        sheetItem['comment_count'] = int(comment_count)
        sheetItem['labels'] = labels
        sheetItem['introduction'] = introduction
        yield sheetItem
        #----------------歌单信息end----------------

        #爬取用户信息
        yield scrapy.Request(url=response.urljoin(user_url), callback=self.parseUser, meta={'id': user_id})

    def parseMusic(self, response):
        pass

    def parseUser(self, response):
        """
            解析用户
        """
        id = response.meta['id']
        data = response.xpath('//div[@class="g-bd"]')

        profile_url = data.xpath('//dt[@id="ava"]/img/@src')[0].extract()

        h2 = data.xpath('//h2[@id="j-name-wrap"]')

        n = h2.xpath('./span/text()').extract()

        name = n[0]
        level = n[1]

        sex_cls = h2.xpath('./i/@class')[0].extract()

        if 'u-icn-01' in sex_cls:
            sex = '男'
        elif 'u-icn-02' in sex_cls:
            sex = '女'
        else:
            sex = '未知'

        moment_count = data.xpath('//*[@id="event_count"]/text()')[0].extract()
        fans_count = data.xpath('//*[@id="fan_count"]/text()')[0].extract()
        follow_count = data.xpath('//*[@id="follow_count"]/text()')[0].extract()

        introduction = data.xpath('//div[@class="inf s-fc3 f-brk"]/text()')
        introduction = introduction[0].extract() if introduction else None

        address = data.xpath('//div[@class="inf s-fc3"]/span/text()')
        address = address[0].extract() if address else None

        age = data.xpath('//div[@class="inf s-fc3"]/span[@id="age"]/@data-age')
        age = time.strftime('%Y-%m-%d', time.gmtime(int(age[0].extract())/1000)) if age else None

        #达人
        data.xpath('//p[@class="djp f-fs1 s-fc3"]/text()')
        data.xpath('//i[@class="tag u-icn2 u-icn2-pfdr"]')
        #V认证
        data.xpath('//i[@class="tag u-icn2 u-icn2-pfv"]')

        userItem = UserItem()
        userItem['id'] = id
        userItem['name'] = name
        userItem['profile_url'] = profile_url
        userItem['level'] = level
        userItem['moment_count'] = moment_count
        userItem['fans_count'] = fans_count
        userItem['follow_count'] = follow_count
        userItem['introduction'] = introduction
        userItem['address'] = address
        userItem['age'] = age
        userItem['sex'] = sex
        yield userItem


