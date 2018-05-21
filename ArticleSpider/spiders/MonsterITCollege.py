# -*- coding: utf-8 -*-
import scrapy


class MonsteritcollegeSpider(scrapy.Spider):
    name = 'MonsterITCollege'
    allowed_domains = ['python.guaishouxueyuan.net']
    start_urls = ['http://python.guaishouxueyuan.net']

    def parse(self, response):
        title_list =  response.xpath('//tbody/tr/th/a[1]/text()').extract()
        with open('Title.txt', 'a') as f:
            for title in title_list:
                f.write(title + '\n')
            f.close()
        next_url = response.css('.nxt::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)


