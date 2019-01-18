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
# 3-进入项目的根目录，执行下列命令启动spider(book_chapter_spider.name属性):
#       scrapy crawl book_chapter_spider
#       scrapy crawl book_chapter_spider -o test.json
# -----------------------------------------------------------------------------------


import scrapy
import pymongo
from scrapy.conf import settings
from BooksSpider.items import BookChapterItem


class BookInfoSpider(scrapy.Spider):
    name = "book_chapter_spider"
    allowed_domains = ["zongheng.com", '17k.com']
    domain_for_zongheng = 'http://hao123.zongheng.com'
    domain_for_17k = 'http://www.17k.com'
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
        book_infos = self.book_info.find(
            {}, {'book_id': 1, 'book_chapter_url': 1})
        for info in book_infos:
            chapter_list_url = info['book_chapter_url']
            print('chapter_list_url->'+chapter_list_url)
            meta_data = {
                'book_id': info['book_id']
            }
            if 'zongheng.com' in chapter_list_url:
                # yield scrapy.Request(url=chapter_url, meta=meta_data, callback=self.parse_chapter_url_for_17k)
                pass
            elif '17k' in chapter_list_url:
                yield scrapy.Request(url= chapter_list_url, meta=meta_data, callback=self.parse_chapter_url_for_17k)
                pass

    # 解析章节地址-17k
    def parse_chapter_url_for_17k(self, response):
        volume_item = response.css('.Volume')
        for sel_volume in volume_item:
            volume_name = sel_volume.css('.tip::text').extract_first()
            response.meta['volume_name'] = volume_name
            chapter_item = sel_volume.css('dd>a::attr(href)').extract()
            for chapter_url in chapter_item:
                print('chapter_url->'+chapter_url)
                yield scrapy.Request(url=self.domain_for_17k + chapter_url, meta=response.meta, callback=self.parse_chapter_info_for_17k)
        pass

     # 解析章节地址-zongzeng
    def parse_chapter_url_for_zongheng(self, response):
        volume_item = response.css('.Volume')
        for sel_volume in volume_item:
            volume_name = sel_volume.css('.tip::text').extract_first()
            response.meta['volume_name'] = volume_name
            chapter_item = sel_volume.css('dd')
            for sel_chapter in chapter_item:
                chapter_url = sel_chapter.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=chapter_url, meta=response.meta, callback=self.parse_chapter_info_for_zongheng)
        pass

    # 解析书信息-17k
    def parse_chapter_info_for_17k(self, response):
        item = BookChapterItem()
        item['book_id'] = response.meta['book_id']
        item['chapter_volume_name'] = response.meta['volume_name']
        item['chapter_id'] = response.url.split('/')[-1].replace('.html', '')
        item['chapter_name'] = ''.join(response.css(
            '.readAreaBox h1::text').extract_first().split()).replace('\r', '').replace('\n', '')
        item['chapter_content'] = ''.join(response.css('.readAreaBox .p::text').extract())
        item['chapter_url'] = response.url
        return item

    # 解析书信息-zongheng
    def parse_chapter_info_for_zongheng(self, response):
        item = BookChapterItem()

        return item
