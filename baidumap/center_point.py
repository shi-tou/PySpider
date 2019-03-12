# -*- coding: UTF-8 -*-

import json
import pymongo

def dealItem(data,type):
    item={}
    item['type']=type
    item['name']=data['n']
    point=data['g'].split('|')[0].split(',')
    item['lng']= float(point[0])
    item['lat']= float(point[1])
    item['zoom']=int(data['g'].split('|')[1])
    return item

# 创建MONGODB数据库链接
client = pymongo.MongoClient(host='139.219.136.96', port=27017)
# 指定数据库
mydb = client['yezi_fang']
region_point=mydb['region_point']
# json.load()函数的使用，将读取json信息
file = open('E:\\bdmap_point.json','r',encoding='utf-8')
info = json.load(file)
items=[]
for p in info['municipalities']:
    item= dealItem(p,'1')
    items.append(item)

for p in info['other']:
    item = dealItem(p,'1')
    items.append(item)

for p in info['provinces']:
    item= dealItem(p,'1')
    items.append(item)
    for c in p['cities']:
        item= dealItem(c,'2')
        items.append(item)
region_point.insert_many(items)


