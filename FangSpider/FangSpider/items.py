# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    project_id = scrapy.Field()
    project_name = scrapy.Field()
    feature = scrapy.Field()  # 特色
    purpose = scrapy.Field()  # 楼盘用途
    avg_price = scrapy.Field()  # 均价
    fitment = scrapy.Field()  # 装修
    developer = scrapy.Field()  # 开发商
    property_company = scrapy.Field()  # 物业公司
    city_id = scrapy.Field()  # 城市id
    area = scrapy.Field()  # 行政区
    address = scrapy.Field()
    lng = scrapy.Field()  # 经度
    lat = scrapy.Field()  # 纬度
    total_house_count = scrapy.Field()  # 总户数
    land_area = scrapy.Field()  # 占地面积
    building_area = scrapy.Field()  # 建筑面积
    green_rate = scrapy.Field()  # 绿化率
    plot_rate = scrapy.Field()  # 容积率
    pass
