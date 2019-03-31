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
#       scrapy crawl budejie_spider
# -----------------------------------------------------------------------------------

from budejie.items import BudejieItem
import scrapy


class BudejieSpider(scrapy.Spider):
    name = "budejie_spider"
    allowed_domains = ["www.budejie.com"]

    def start_requests(self):
        url = 'http://www.budejie.com/'
        for i in range(1, 10):
            yield scrapy.Request(url=url + str(i + 1), callback=self.parse)

    # 解析【不得姐】列表
    def parse(self, response):
        items = []
        list_tool = response.css(".j-r-list-tool")
        list_c = response.css(".j-r-list-c")
        index = 0
        for v in list_tool:
            item = BudejieItem()
            item["title"] = v.css("::attr(data-title)").extract_first()
            item["time"] = v.css("::attr(data-date)").extract_first().replace("-", "")
            item["img_url"] = list_c[index].css("img.lazy::attr(data-original)").extract_first()
            items.append(item)
            index += 1
        return items
