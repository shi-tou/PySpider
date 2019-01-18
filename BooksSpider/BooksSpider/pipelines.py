# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.conf import settings


class BooksspiderPipeline(object):
    def __init__(self):
        # 1-文件存储
        #self.file = codecs.open('blogs.json', 'wb', encoding='utf-8')

        # 2-mongodb存储
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.book_info = mydb['book_info']
        self.book_chapter = mydb['book_chapter']

    def process_item(self, item, spider):
        if(spider.name == 'book_info_spider'):
            if(self.book_info.find({'book_id': item['book_id']}).count() == 0):
                self.book_info.insert(dict(item))
        elif(spider.name=='book_chapter_spider'):
            if(self.book_chapter.find({'chapter_id': item['chapter_id']}).count() == 0):
                self.book_chapter.insert(dict(item))
            pass
        return item
