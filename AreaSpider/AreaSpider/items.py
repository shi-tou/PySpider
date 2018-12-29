# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProvinceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province_code=scrapy.Field()
    province_name=scrapy.Field()
    source_url=scrapy.Field()
    pass

class CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province_code = scrapy.Field()
    city_code=scrapy.Field()
    city_name=scrapy.Field()
    source_url=scrapy.Field()
    pass

class AreaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province_code = scrapy.Field()
    city_code = scrapy.Field()
    area_code = scrapy.Field()
    area_name = scrapy.Field()
    source_url=scrapy.Field()
    pass

class SubAreaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province_code = scrapy.Field()
    city_code = scrapy.Field()
    area_code = scrapy.Field()
    sbuarea_code = scrapy.Field()
    subarea_name=scrapy.Field()
    source_url=scrapy.Field()
    pass