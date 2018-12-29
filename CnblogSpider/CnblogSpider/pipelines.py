# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pymongo
from scrapy.conf import settings

class CnblogspiderPipeline(object):
    def __init__(self):
        # 1-文件存储
        #self.file = codecs.open('blogs.json', 'wb', encoding='utf-8')

        # 2-mongodb存储
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.articles = mydb[sheetname]

    def process_item(self, item, spider):
        # 1-文件存储
        # line = json.dumps(dict(item),ensure_ascii=False) + ','
        # self.file.write(line)
        
        #2-mongodb存储
        if(self.articles.find({'article_id':item['article_id']}).count() > 0):
            self.articles.update({"article_id":item['article_id']},dict(item))
        else:
            self.articles.insert(dict(item))
        return item

    #def spider_closed(self, spider):
        #关闭文件
        #self.file.close()