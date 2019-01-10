# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 书id
    book_id = scrapy.Field()
    # 书名
    book_name = scrapy.Field()
    # 作者
    book_author = scrapy.Field()
    # 类别
    book_type_name = scrapy.Field()
    # 封面图片
    book_image_url = scrapy.Field()
    # 简介
    book_summary = scrapy.Field()
    # 简介地址
    book_summary_url = scrapy.Field()
    # 总字数
    book_word_count = scrapy.Field()
    # 章节地址
    book_chapter_url = scrapy.Field()
    # 来源站点名称
    source_site_name = scrapy.Field()
    # 来源站点地址
    source_site_url = scrapy.Field()
    pass

class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 书id
    book_id = scrapy.Field()
    # 书名
    book_name = scrapy.Field()
    # 作者
    book_author = scrapy.Field()
    # 类别
    book_type_name = scrapy.Field()
    # 封面图片
    book_image_url = scrapy.Field()
    # 简介
    book_summary = scrapy.Field()
    # 简介地址
    book_summary_url = scrapy.Field()
    # 总字数
    book_word_count = scrapy.Field()
    # 章节地址
    book_chapter_url = scrapy.Field()
    # 来源站点名称
    source_site_name = scrapy.Field()
    # 来源站点地址
    source_site_url = scrapy.Field()
    pass
