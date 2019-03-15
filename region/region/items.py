# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RegionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 省
    province_code=scrapy.Field()
    province_name = scrapy.Field()
    # 市
    city_code = scrapy.Field()
    city_name = scrapy.Field()
    # 区
    district_code = scrapy.Field()
    district_name = scrapy.Field()
    # 街道
    street_code = scrapy.Field()
    street_name = scrapy.Field()
    # 居委会
    village_code = scrapy.Field()
    village_name = scrapy.Field()

    pass
