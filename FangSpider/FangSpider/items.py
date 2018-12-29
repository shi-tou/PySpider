# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ProjectResponseItem(scrapy.Item):
    scrapy.Field()

class ProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    project_id = scrapy.Field()
    project_name = scrapy.Field()
    project_developer = scrapy.Field()
    pre_sale_permit_number = scrapy.Field()
    approval_time = scrapy.Field()
    approval_department = scrapy.Field()
    land_no = scrapy.Field()
    land_address = scrapy.Field()
    contract_no = scrapy.Field()
    usable_year = scrapy.Field()
    house_purpose = scrapy.Field()
    land_purpose = scrapy.Field()
    land_area = scrapy.Field()
    building_area = scrapy.Field()
    pre_sale_total_number = scrapy.Field()
    pre_sale_total_area = scrapy.Field()
    city_name = scrapy.Field()
    area_name = scrapy.Field()
    property_company_name = scrapy.Field()
    property_fee = scrapy.Field()
    phone1 = scrapy.Field()
    phone2 = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    update_time = scrapy.Field()
    source_name = scrapy.Field()
    source_url = scrapy.Field()
    pass

class ToBeClean_ProjectItem(ProjectItem):
    building_data = scrapy.Field()
    pass

class BuildingItem(scrapy.Item):
    project_id = scrapy.Field()#楼盘id
    building_id = scrapy.Field()#楼栋id
    building_name=scrapy.Field()#楼栋名
    building_planning_permit_no=scrapy.Field()# 建设工程规划许可证
    building_construction_permit_no=scrapy.Field()# 建筑工程施工许可证
    source_url = scrapy.Field()
    pass
