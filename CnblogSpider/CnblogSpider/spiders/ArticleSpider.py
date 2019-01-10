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
# 3-进入项目的根目录，执行下列命令启动spider(cnblog_spider为定义的spider.name属性):
#       scrapy crawl cnblog_spider
#       scrapy crawl cnblog_spider -o test.json
# -----------------------------------------------------------------------------------


import scrapy
import re
from CnblogSpider.items import CnblogspiderItem


class ArticleSpider(scrapy.Spider):
    name = "cnblog_spider"
    allowed_domains = ["cnblogs.com"]

    def start_requests(self):
        urls = []
        for i in range(1, 200):
            urls.append("https://www.cnblogs.com/sitehome/p/"+str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        post_item= response.css('.post_item')
        for sel in post_item:
            item = CnblogspiderItem()
            #文章id，文章链接
            str_article_url=sel.css(
                '.titlelnk::attr(href)').extract_first()
            item['article_id'] =str_article_url.split('/')[-1].replace('.html','')
            print(str_article_url.split('/')[-1])
            item['article_url'] = str_article_url
            #文章标题
            item['article_title'] = sel.css('.titlelnk::text').extract_first()
            #作者
            item['article_author'] = sel.css(
                '.lightblue::text').extract_first()
            #文章摘要
            article_summary = sel.css('.post_item_summary::text').extract()
            if(len(article_summary)==1):
                item['article_summary'] =article_summary[0].replace('\r\n', '').strip()
            else:
                item['article_summary'] =article_summary[1].replace('\r\n', '').strip()
            #发布时间
            item['article_posttime'] = sel.css('.post_item_foot::text').extract()[1].replace('\r\n', '').replace('发布于', '').strip()
            #推荐数
            item['article_recommend_count'] = sel.css(
                '.diggnum::text').extract_first()
            # 评论数
            str_comment_count = sel.css('.article_comment a::text').extract_first().replace('\r\n', '').strip()
            item['article_comment_count'] = re.findall(r'[^()]+', str_comment_count)[1]
            # 阅读数
            str_view_count = sel.css('.article_view a::text').extract_first().replace('\r\n', '').strip()
            item['article_view_count'] = re.findall(r'[^()]+', str_view_count)[1]
            # filename = response.url.split("/")[-2]
            # with open(filename, 'wb') as f:
            #     f.write(response.body)
            items.append(item)
        return items
