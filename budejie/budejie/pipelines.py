# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests


class BudejiePipeline(object):
    base_dir = "F:\\budejie\\"
    header = {
        'USER-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie': 'b963ef2d97e050aaf90fd5fab8e78633',
        # 需要查看图片的cookie信息，否则下载的图片无法查看
    }

    def process_item(self, item, spider):
        title = item["title"]
        img_url = item["img_url"]
        time = item["time"]

        file_name = title + os.path.splitext(img_url)[-1]
        file_dir = self.base_dir + time

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        with open('{}\\{}'.format(file_dir, file_name), 'wb') as f:
            req = requests.get(img_url, headers=self.header)
            f.write(req.content)
        return item
