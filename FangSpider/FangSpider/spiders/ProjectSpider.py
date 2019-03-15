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
#       scrapy crawl project_spider
# -----------------------------------------------------------------------------------

from FangSpider.items import ProjectItem
from FangSpider.common import Utils
import scrapy


class FangSpider(scrapy.Spider):
    name = "project_spider"
    allowed_domains = ["xy.zp365.com"]
    domain = "http://xy.zp365.com"
    city_id = 226

    page_count = 1

    def start_requests(self):
        for i in range(self.page_count):
            url = self.domain + "/NewHouse/index?houseType=1&pageIndex=" + str(i + 1)
            yield scrapy.Request(url=url, callback=self.parse)

    # 解析楼盘列表
    def parse(self, response):
        list_item = response.css(".nhlist-item")
        for item in list_item:
            pid = item.css('.join-contrast::attr(data-id)').extract_first()
            url = item.css('.img::attr(href)').extract_first() + "&sid=2"
            yield scrapy.Request(url=self.domain + url, meta={"pid": pid}, callback=self.parse_info)

    # 解析楼盘详情
    def parse_info(self, response):
        item = ProjectItem()
        item["project_id"] = response.meta["pid"]
        item["project_name"] = response.css('dt:contains("楼盘名称") + dd::text').extract_first()
        item["feature"] = ','.join(response.css('dt:contains("楼盘特色") +dd span::text').extract())
        new_purpose = []
        purpose = response.css('dt:contains("物业类型") +dd span::text').extract()
        for p in purpose:
            new_purpose.append(p.strip())
        item["purpose"] = ','.join(new_purpose)
        item["avg_price"] = Utils.str_to_float(response.css('.price::text').extract_first())
        item["fitment"] = response.css('dt:contains("装修情况") + dd::text').extract_first()
        item["developer"] = Utils.filter_html(response.css('dt:contains("开发商") + dd::text').extract_first())
        item["property_company"] = Utils.filter_html(response.css('dt:contains("物业公司") + dd::text').extract_first())
        item["city_id"] = self.city_id
        item["area"] = response.css('dt:contains("所在城区") + dd::text').extract_first()
        item["address"] = response.css('dt:contains("销售位置") + dd::text').extract_first()
        item["lng"] = Utils.str_to_float(response.css('.map::attr(data-baidulng)').extract_first())
        item["lat"] = Utils.str_to_float(response.css('.map::attr(data-baidulat)').extract_first())
        item["total_house_count"] = Utils.str_to_int(response.css('dt:contains("总 户 数") + dd::text').extract_first())
        item["land_area"] = Utils.str_to_float(response.css('dt:contains("总 占 地") + dd::text').extract_first())
        item["building_area"] = Utils.str_to_float(response.css('dt:contains("建筑面积") + dd::text').extract_first())
        item["green_rate"] = Utils.str_to_float(response.css('dt:contains("绿 化 率") + dd::text').extract_first())
        item["plot_rate"] = Utils.str_to_float(response.css('dt:contains("容 积 率") + dd::text').extract_first())
        return item
