# -*- coding: UTF-8 -*-
# need import：pip install mysql-connector-python

import json
import pymongo
import mysql.connector



class syncdata:
    
    # 创建MONGODB数据库链接
    client = pymongo.MongoClient(host='139.219.136.96', port=27017)
    # 指定数据库
    mymongodb = client['yezi_fang']
    region = mymongodb['region']

    mysqldb = mysql.connector.connect(
        host="localhost",       # 数据库主机地址
        user="root",    # 数据库用户名
        passwd="123",   # 数据库密码
        database="yezi_fang" #数据库名
    )
    cursor = mysqldb.cursor()

    def getRegion(self):
        return self.region.find({})

    def insertRegion(self,item):
        sql = "INSERT INTO t_region (province_code, province_name, city_code, city_name, district_code, district_name, street_code, street_name, village_code, village_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.cursor.execute(sql, item)
        self.mysqldb.commit()

m = syncdata()
regionData=m.getRegion()
for p in regionData:
    item=dict(p)
    # 去掉"_id" 列
    item.pop('_id')
    m.insertRegion(tuple(item.values()))
m.mysqldb.close()