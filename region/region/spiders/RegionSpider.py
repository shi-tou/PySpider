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
#       创建一个scrapy项目scrapy startproject mingyan
#       scrapy crawl region_spider
# -----------------------------------------------------------------------------------

from region.items import RegionItem
import scrapy


class RegionSpider(scrapy.Spider):
    name = "region_spider"
    allowed_domains = ["stats.gov.cn"]
    main_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'

    def start_requests(self):
        yield scrapy.Request(url=self.main_url + 'index.html', callback=self.parse)

    def parse(self, response):
        for sel in response.css('.provincetr a'):
            source_url = self.main_url + sel.css('::attr(href)').extract_first()
            province_name = sel.css('::text').extract_first()
            province_code= source_url.split('/')[-1].replace('.html', '')
            meta_data = {
                'province_name': province_name,
                'province_code': province_code
            }
            yield scrapy.Request(url=source_url, meta=meta_data, callback=self.parse_city)

    def parse_city(self, response):
        meta_data = response.meta
        for sel in response.css('.citytr'):
            city_name = sel.css('td:nth-child(2) a::text').extract_first()
            city_code = sel.css('td:nth-child(1) a::text').extract_first()
            source_url = sel.css('td:nth-child(1) a::attr(href)').extract_first()
            if source_url is None:
                continue
            meta_data['city_name'] = city_name
            meta_data['city_code'] = city_code
            yield scrapy.Request(url=response.url[:response.url.rfind("/")+1] +source_url, meta=meta_data, callback=self.parse_district)

    def parse_district(self, response):
        meta_data = response.meta
        for sel in response.css('.countytr'):
            district_name = sel.css('td:nth-child(2) a::text').extract_first()
            district_code = sel.css('td:nth-child(1) a::text').extract_first()
            source_url = sel.css('td:nth-child(1) a::attr(href)').extract_first()
            if source_url is None:
                continue
            meta_data['district_name'] = district_name
            meta_data['district_code'] = district_code
            yield scrapy.Request(url=response.url[:response.url.rfind("/")+1] + source_url, meta=meta_data, callback=self.parse_street)

    def parse_street(self, response):
        meta_data = response.meta
        for sel in response.css('.towntr'):
            street_name = sel.css('td:nth-child(2) a::text').extract_first()
            street_code = sel.css('td:nth-child(1) a::text').extract_first()
            source_url = sel.css('td:nth-child(1) a::attr(href)').extract_first()
            if source_url is None:
                continue
            meta_data['street_name'] = street_name
            meta_data['street_code'] = street_code
            yield scrapy.Request(url=response.url[:response.url.rfind("/")+1] + source_url, meta=meta_data, callback=self.parse_village)

    def parse_village(self, response):
        items = []
        meta_data = response.meta
        for sel in response.css('.villagetr'):
            item = RegionItem()
            item['province_code']=meta_data['province_code']
            item['province_name'] = meta_data['province_name']
            item['city_code'] = meta_data['city_code']
            item['city_name'] = meta_data['city_name']
            item['district_code'] = meta_data['district_code']
            item['district_name'] = meta_data['district_name']
            item['street_code'] = meta_data['street_code']
            item['street_name'] = meta_data['street_name']
            village_name = sel.css('td:nth-child(3)::text').extract_first()
            village_code = sel.css('td:nth-child(1)::text').extract_first()
            item['village_code'] = village_code
            item['village_name'] = village_name
            items.append(item)
        return items