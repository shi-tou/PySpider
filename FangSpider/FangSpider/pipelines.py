# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pymongo
from scrapy.conf import settings
from FangSpider.items import BuildingItem

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
        self.projects = mydb['projects']
        self.buildings = mydb['buildings']

    def process_item(self, item, spider):
        if(spider.name=='project_spider'):
            # 处理楼盘
            dict_data=dict(item)
            dict_data.pop('building_data')
            if(self.projects.find({'project_id':item['project_id']}).count() > 0):
                self.projects.update({"project_id":item['project_id']},dict_data)
            else:
                self.projects.insert(dict_data)
            # 处理楼栋
            buildingItems = item["building_data"]
            for buildingItem in buildingItems:
                if(self.buildings.find({'building_id':buildingItem['building_id']}).count() > 0):
                    self.buildings.update({"building_id":buildingItem['building_id']},dict(buildingItem))
                else:
                    self.buildings.insert(dict(buildingItem))
        return item

    def spider_closed(self, spider):
        #关闭文件
        #self.file.close()
        pass