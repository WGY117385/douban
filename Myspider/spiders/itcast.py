# -*- coding: utf-8 -*-
import json

import scrapy

from ..items import MyspiderItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=20']
    offset = 0
    def parse(self, response):

        content_list = json.loads(response.body.decode())
        if content_list == []:
            return
        for content in content_list:
            item = MyspiderItem()
            item['title'] = content["title"]
            item['url'] = content["url"]
            yield scrapy.Request(url = item['url'],callback=self.parse_data,meta={"item":item})

        self.offset += 20
        url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start='+str(self.offset) + '&limit=20'
        yield scrapy.Request(url = url,callback=self.parse)


    def parse_data(self,response):

        item = response.meta["item"]
        data_list = response.xpath('//div[@id="info"]')
        for data in data_list:
            item["daoyan"] = data.xpath('./span[1]/span[@class="attrs"]').xpath('string(.)').extract_first()
            item["bianju"] = data.xpath('./span[2]/span[@class="attrs"]').xpath('string(.)').extract_first()
            item["zhuyan"] = data.xpath('./span[3]/span[@class="attrs"]').xpath('string(.)').extract_first()
            item["pianchang"] = data.xpath('./span[@property="v:runtime"]/text()').extract_first()

        print(item,37)
        yield item
        item = {}