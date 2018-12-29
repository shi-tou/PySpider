# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import pymongo
from scrapy.conf import settings

class AreaspiderPipeline(object):
    def __init__(self):
        # 1-文件存储
        self.file = codecs.open('area.json', 'wb', encoding='utf-8')
        # 2-mongodb存储
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        self.mydb = client[dbname]
        self.province = self.mydb['province']
        self.city = self.mydb['city']
        self.area = self.mydb['area']
        self.subarea = self.mydb['subarea']

    def process_item(self, item, spider):
        # 1-文件存储
        line = json.dumps(dict(item),ensure_ascii=False) + ','
        self.file.write(line)

        if(spider.name=='province_spider'):
            # 存放数据的数据库表名
            if(self.province.find({'province_code':item['province_code']}).count() > 0):
                self.province.update({"province_code":item['province_code']},dict(item))
            else:
                self.province.insert(dict(item))
        elif(spider.name=='city_spider'):
            # 存放数据的数据库表名
            if(self.city.find({'city_code':item['city_code']}).count() > 0):
                self.city.update({"city_code":item['city_code']},dict(item))
            else:
                self.city.insert(dict(item))
        elif(spider.name=='area_spider'):
            # 存放数据的数据库表名
            if(self.area.find({'area_code':item['area_code']}).count() > 0):
                self.area.update({"area_code":item['area_code']},dict(item))
            else:
                self.area.insert(dict(item))
        return item

    def spider_closed(self, spider):
        #关闭文件
        self.file.close()
