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
#       scrapy crawl project_spider
# -----------------------------------------------------------------------------------

import json
import scrapy
from urllib import parse
from FangSpider.items import ToBeClean_ProjectItem
from FangSpider.items import BuildingItem


class FangSpider(scrapy.Spider):
    name = "project_spider"
    allowed_domains = ["ris.szpl.gov.cn"]
    domain = "http://ris.szpl.gov.cn/bol/"
    project_list_url = domain + "/index.aspx"
    project_detail_url = domain + "/projectdetail.aspx?id="
    __EVENTTARGET = 'AspNetPager1'
    __VIEWSTATE = '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'
    __EVENTVALIDATION = 'azRsa0h+YGNyYngP55wXIqZznGWlVQybSCwGf1qxYlMd0Zs2Z7pCstew63rz6N4HGPkfGQXdepEmF6VC+ZsH4XhM5a53TXrtZTHuI9i/0a6Z8ijCiHY/ZrHEvr4MJNcTB+JA4XTEvYBxGvfhjnuT+V9yqxKaeko0ECb5D4cRrH94oWfN'
    # header信息
    # header = {
    #     'Host': 'ris.szpl.gov.cn'
    # }

    def start_requests(self):

        for i in range(1, 110):
            if(i == 1):
                yield scrapy.Request(url=self.project_list_url, callback=self.parse_list)
            else:
                form_data = {
                    '__EVENTTARGET': self.__EVENTTARGET,
                    '__EVENTARGUMENT': str(i),
                    'AspNetPager1_input': '1',
                    '__VIEWSTATE': self.__VIEWSTATE,
                    '__EVENTVALIDATION': self.__EVENTVALIDATION,
                    '__VIEWSTATEENCRYPTED': ''
                }
                yield scrapy.FormRequest(url=self.project_list_url, method='POST', formdata=form_data, callback=self.parse_list, dont_filter=True)

    # 解析列表
    def parse_list(self, response):
        project_item = response.css('#DataList1 tr[bgcolor="#F5F9FC"]')
        for sel in project_item:
            # 预售证号
            pre_sale_permit_number = sel.css(
                'td:nth-child(2) a::text').extract_first()
            # 楼盘id
            source_url = sel.css(
                'td:nth-child(3) a::attr(href)').extract_first()
            project_id = source_url.split('=')[-1]
            # 开发商
            project_developer = sel.css(
                'td:nth-child(4)::text').extract_first()
            # 批准时间
            approval_time = sel.css(
                'td:nth-child(6)::text').extract_first()
            meta_data = {
                'project_id': project_id,
                'pre_sale_permit_number': pre_sale_permit_number,
                'project_developer': project_developer,
                'approval_time': approval_time
            }
            yield scrapy.Request(url=self.project_detail_url+project_id, meta=meta_data, callback=self.parse_detail)

    # 解析详情
    def parse_detail(self, response):
        project_id = response.meta['project_id']
        pre_sale_permit_number = response.meta['pre_sale_permit_number']
        approval_time = response.meta['approval_time']
        project_developer = response.meta['project_developer']
        tr_item = response.css('.a1')
        item = ToBeClean_ProjectItem()
        item['project_id'] = project_id
        item['pre_sale_permit_number'] = pre_sale_permit_number
        item['project_developer'] = project_developer
        item['approval_time'] = approval_time
        item['approval_department'] = tr_item.css(
            'td:contains("批准机关") + td div::text').extract_first()
        item['source_url'] = response.url
        item['project_name'] = tr_item.css(
            'td:contains("项目名称") + td::text').extract_first()
        item['city_name'] = '深圳'
        item['area_name'] = tr_item.css(
            'td:contains("所在区域") + td::text').extract_first()
        item['land_no'] = tr_item.css(
            'td:contains("宗地号") + td::text').extract_first()
        item['land_address'] = tr_item.css(
            'td:contains("宗地位置") + td::text').extract_first()
        item['contract_no'] = tr_item.css(
            'td:contains("合同文号") + td::text').extract_first()
        item['usable_year'] = tr_item.css(
            'td:contains("使用年限") + td div::text').extract_first().replace('\r\n', '').strip()
        item['house_purpose'] = tr_item.css(
            'td:contains("房屋用途") + td::text').extract_first()
        item['land_purpose'] = tr_item.css(
            'td:contains("土地用途") + td::text').extract_first()
        item['land_area'] = tr_item.css(
            'td:contains("宗地面积") + td::text').extract_first()
        item['building_area'] = tr_item.css(
            'td:contains("总建筑面积") + td::text').extract_first()
        item['pre_sale_total_number'] = tr_item.css(
            'td:contains("预售总套数") + td::text').extract_first()
        item['pre_sale_total_area'] = tr_item.css(
            'td:contains("预售总面积") + td::text').extract_first()
        item['property_company_name'] = tr_item.css(
            'td:contains("物业管理公司") + td::text').extract_first()
        item['property_fee'] = tr_item.css(
            'td:contains("管理费") + td::text').extract_first()
        item['phone1'] = tr_item.css(
            'td:contains("售楼电话一") + td::text').extract_first()
        item['phone2'] = tr_item.css(
            'td:contains("售楼电话二") + td::text').extract_first()
        building_item = response.css('#DataList1 tr[bgcolor="#F5F9FC"]')
        buildingData = []

        for sel in building_item:
            data = BuildingItem()
            data['project_id'] = project_id
            # 楼栋名
            data['building_name'] = sel.css(
                'td:nth-child(2)::text').extract_first()
            # 建设工程规划许可证
            data['building_planning_permit_no'] = sel.css(
                'td:nth-child(3)::text').extract_first()
            # 建筑工程施工许可证
            data['building_construction_permit_no'] = sel.css(
                'td:nth-child(4)::text').extract_first()
            source_url = sel.css(
                'td:nth-child(5) a::attr(href)').extract_first()
            url_data = parse.urlparse(source_url)
            data['building_id'] = parse.parse_qs(url_data.query)['id'][0]
            data['source_url'] = source_url
            buildingData.append(data)
        item['building_data'] = buildingData
        return item
