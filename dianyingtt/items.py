# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DyttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weburl = scrapy.Field()
    tname = scrapy.Field() #翻译名称
    oname = scrapy.Field() #原名
    year = scrapy.Field() #年代
    country = scrapy.Field() #国家
    category = scrapy.Field() #类别
    language = scrapy.Field() # 语言
    word = scrapy.Field() #字幕
    issuedata = scrapy.Field()
    imdb = scrapy.Field()
    douban = scrapy.Field()
    fileformat = scrapy.Field()
    movielens = scrapy.Field()
    director = scrapy.Field()
    ftpurl = scrapy.Field()#下载地址

