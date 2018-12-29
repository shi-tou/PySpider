# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    article_author = scrapy.Field()
    article_summary = scrapy.Field()
    article_posttime = scrapy.Field()
    article_recommend_count = scrapy.Field()
    article_comment_count = scrapy.Field()
    article_view_count = scrapy.Field()
    pass
