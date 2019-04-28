# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect


class MyspiderPipeline(object):
    def __init__(self):
        self.db = connect(host='172.105.220.160', port=3306, user='root', database='WGY', password='hb_root123456', charset='utf8')

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        sql = 'insert into douban (title,url,daoyan,bianju,zhuyan,pianchang) values ("{}","{}","{}","{}","{}","{}")'.format(item['title'],item['url'],item['daoyan'],item['bianju'],item['zhuyan'],item['pianchang'])
        cursor.execute(sql)
        self.db.commit()
        return item
