# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy.item import Item

class dianyingttPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URI = crawler.settings.get('MONGO_DB_URI','mongodb://localhost:27017/')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_default')
        cls.DB_COLLECTION = crawler.settings.get('MONGODB_COLLECTION', 'COLLECTION_default')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[self.DB_COLLECTION]
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        return item
    
# 去重
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    def __init__(self):
        self.weburl_set = set()

    def process_item(self, item, spider):
        weburl = item['weburl']
        name = item['tname']
        if weburl in self.weburl_set:
            raise DropItem("重复电影: %s" % name)
        self.weburl_set.add(weburl)
        return item

# mysql
import MySQLdb

class MySQLPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')
        self.table = spider.settings.get('MYSQL_TABLE', 'table_default')

        self.db_conn = MySQLdb.connect(host=host, port=port, db=db,user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()
        
        # 如果数据表已经存在使用 execute() 方法删除表。
        self.db_cur.execute("DROP TABLE IF EXISTS "+self.table)
        sql = """CREATE TABLE """+self.table+""" (
            weburl VARCHAR(256) NOT NULL PRIMARY KEY,
            tname VARCHAR(256) NOT NULL,
            oname VARCHAR(256) NOT NULL,
            year  VARCHAR(256) NOT NULL,
            country VARCHAR(256) NOT NULL,
            category VARCHAR(256) NOT NULL,
            language VARCHAR(256) NOT NULL,
            word VARCHAR(256) NOT NULL,
            issuedata VARCHAR(256) NOT NULL,
            imdb VARCHAR(256) NOT NULL,
            douban VARCHAR(256) NOT NULL,
            fileformat VARCHAR(256) NOT NULL,
            movielens VARCHAR(256) NOT NULL,
            director VARCHAR(256) NOT NULL,
            ftpurl VARCHAR(256) NOT NULL         
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        self.db_cur.execute(sql)


    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item


    def insert_db(self, item):
        values = (
        item['weburl'],
        item['tname'],
        item['oname'],
        item['year'],
        item['country'],
        item['category'],
        item['language'],
        item['word'],
        item['issuedata'],
        item['imdb'],
        item['douban'],
        item['fileformat'],
        item['movielens'],
        item['director'],
        item['ftpurl']
        )
        sql = 'INSERT INTO '+self.table+' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)