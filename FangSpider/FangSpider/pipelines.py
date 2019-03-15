# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings


class FangspiderPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.project = mydb['project']

    def process_item(self, item, spider):
        dict_data = dict(item)
        if (self.project.find({'project_id': item['project_id']}).count() > 0):
            self.project.update({"project_id": item['project_id']}, dict_data)
        else:
            self.project.insert(dict_data)
        return item
