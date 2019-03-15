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
# 3-进入项目的根目录，执行下列命令启动spider(test_spider为定义的spider.name属性):
#       scrapy crawl building_spider
# -----------------------------------------------------------------------------------

import json
import scrapy
import pymongo
from scrapy.conf import settings
from FangSpider.items import HouseItem


class FangSpider(scrapy.Spider):
    name = "building_spider"
    allowed_domains = ["ris.szpl.gov.cn"]
    domain = "http://ris.szpl.gov.cn/bol/"

    host = settings["MONGODB_HOST"]
    port = settings["MONGODB_PORT"]
    dbname = settings["MONGODB_DBNAME"]
    # 创建MONGODB数据库链接
    client = pymongo.MongoClient(host=host, port=port)
    # 指定数据库
    mydb = client[dbname]
    # 存放数据的数据库表名
    buildings = mydb['buildings']
    houses = mydb['houses']

    def start_requests(self):
        for c in self.buildings.find({}):
            meta_data = {
                'project_id': c['project_id'],
                'building_id': c['building_id']
            }
            yield scrapy.Request(url=self.domain + c['source_url'], meta=meta_data, callback=self.parse_branch)

    # 解析座号
    def parse_branch(self, response):
        branchName = []
        branch_item = response.css('#divShowBranch a')
        for sel in branch_item:
            branchName.append(sel.css('::text').extract_first().replace(
                '[', '').replace(']', ''))
        branchName.append(response.css(
            '#divShowBranch font::text').extract_first().replace('[', '').replace(']', ''))

        for _item in branchName:
            response.meta['unit_name'] = _item
            yield scrapy.Request(url=response.url+"&Branch="+_item, meta=response.meta, callback=self.parse_house_url)
        pass

    # 解析房号
    def parse_house_url(self, response):
        house_url_item = response.css('#divShowList a')
        for sel in house_url_item:
            yield scrapy.Request(url=self.domain + str(sel.css('::attr(href)').extract_first()), meta=response.meta, callback=self.parse_house_detail)
        pass

    def parse_house_detail(self, response):
        project_id = response.meta['project_id']
        building_id = response.meta['building_id']
        unit_name = response.meta['unit_name']
        tr_item = response.css('.a1')
        item = HouseItem()
        item['house_id'] = response.url.split('=')[-1]
        item['project_id'] = project_id
        item['building_id'] = building_id
        item['unit_name'] = unit_name
        item['house_name'] = ''.join(tr_item.css(
            'td:contains("房号") + td::text').extract_first().split())
        item['floor_no'] = ''.join(tr_item.css(
            'td:contains("楼层") + td::text').extract_first().split())
        item['house_purpose'] = ''.join(tr_item.css(
            'td:contains("用途") + td::text').extract_first().split())
        item['build_area'] = tr_item.css(
            'td:contains("建筑面积") + td::text').extract_first()
        item['indoor_area'] = tr_item.css(
            'td:contains("户内面积") + td::text').extract_first()
        item['share_area'] = tr_item.css(
            'td:contains("分摊面积") + td::text').extract_first()
        item['price'] = tr_item.css(
            'td:contains("备案价格") + td::text').extract_first().replace('\r','').replace('\t','').replace('\n','')
        item['contract_no'] = "".join(tr_item.css(
            'td:contains("合同号") + td::text').extract_first().split()).replace('\r','').replace('\t','').replace('\n','')
        return item
