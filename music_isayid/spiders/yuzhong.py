import re
import scrapy
from music_isayid.items import SheetItem
import music_isayid.settings as settings

class Yuzhong(scrapy.Spider):
    """
    语种spider
    """
    name = 'yuzhong'
    allow_domain = 'https://music.163.com/'
    baseurl = 'https://music.163.com/discover/playlist/?cat='
    sub_names = ['华语']
    #sub_names = ['华语', '欧美', '日语', '韩语', '粤语', '小语种']

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
            if int(players[index].replace('万', '0000')) >= settings.SHEET_MIN_PLAYER:
                yield scrapy.Request(url=response.urljoin(sheet_url), callback=self.parseSheet,
                                 meta={id: re.search('\d+', sheet_url).group(0)})

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


