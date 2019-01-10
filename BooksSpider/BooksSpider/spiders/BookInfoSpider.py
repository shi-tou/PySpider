# -*- coding: UTF-8 -*-
# --------------------------------------------------------------------------------
# 说明：
# 1-Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。
# 2-为了创建一个Spider，您必须继承 scrapy.Spider 类， 且定义以下三个属性:
#   【name】: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
#   【start_urls】: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将
#       是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
#   【parse()】： 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对
#       象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数
#       据(生成item)以及生成需要进一步处理的URL的 Request 对象。
# 3-进入项目的根目录，执行下列命令启动spider(book_info_spider.name属性):
#       scrapy crawl book_info_spider
#       scrapy crawl book_info_spider -o test.json
# -----------------------------------------------------------------------------------


import scrapy
import pymongo
from scrapy.conf import settings

class BookInfoSpider(scrapy.Spider):
    name = "book_info_spider"
    allowed_domains = ["zongheng.com"]
    host = settings["MONGODB_HOST"]
    port = settings["MONGODB_PORT"]
    dbname = settings["MONGODB_DBNAME"]
    # 创建MONGODB数据库链接
    client = pymongo.MongoClient(host=host, port=port)
    # 指定数据库
    mydb = client[dbname]
    # 存放数据的数据库表名
    book_info = mydb['book_info']

    def start_requests(self):
        urls = []
        book_infos=self.book_info.find({})

        for info in book_infos:
            if 'zongheng.com' in info['book_chapter_url']:
                urls.append(info['book_chapter_url'])
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_chapter_url)
    
    # 解析章节地址
    def parse_chapter_url(self, response):
        book_url_item = response.css('.infos>h2>a::attr(href)').extract()
        for sel in book_url_item:
            yield scrapy.Request(url=sel, callback=self.parse_book_info)
        pass
    # 解析书信息

    def parse_book_info(self, response):
        item = BooksInfoItem()
        item['book_id'] = response.url.split('/')[-1].replace('.html', '')
        # 书名
        item['book_name'] = response.css(
            '.book_infos>h1>a::text').extract_first()
        # 作者
        item['book_author'] = response.css(
            '.binfos>span:nth-child(1)>a::text').extract_first()
        # 类别
        item['book_type_name'] = response.css(
            '.binfos>span:nth-child(2)>a::text').extract_first()

        # 封面图片
        item['book_image_url'] = response.css(
            '.book_face img::attr(src)').extract_first()
        # 简介
        item['book_summary'] = response.css(
            '.cons_all::attr(title)').extract_first()
        # 简介地址
        item['book_summary_url'] = response.url
        # 总字数
        item['book_word_count'] = response.css(
            '.binfos>span:nth-child(5)>b::text').extract_first()
        # 章节地址
        item['book_chapter_url'] = response.css(
            '.book_infos>h1>a::attr(href)').extract_first()
        # 来源站点名称
        item['source_site_name'] = response.css(
            '.binfos>span:nth-child(3)>a::text').extract_first()
        # 来源站点地址
        item['source_site_url'] = response.css(
            '.binfos>span:nth-child(3)>a::attr(href)').extract_first()
        return item
