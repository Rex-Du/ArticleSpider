# -*- coding: utf-8 -*-
import re
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# 分发器
from scrapy.xlib.pydispatch import dispatcher
# 信号
from scrapy import signals

from items import LagouJobItem, LagouJobItemLoader
from utils.common import get_md5
from settings import SQL_DATETIME_FORMAT
from selenium import webdriver

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe', chrome_options=self.chrome_options)
        super(LagouSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        # 当爬虫关闭的时候，关掉chrom浏览器
        print('spider closed!')
        self.browser.quit()


    rules = (
        # Rule(LinkExtractor(allow=('zhaopin/.*', )), follow=True),
        # Rule(LinkExtractor(allow=('gongsi/j\d+.html')), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400',
        'Host': 'www.lagou.com',
        'Upgrade-Insecure-Requests': '1'
    }

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, dont_filter=True, headers=self.headers)
    #
    # def _build_request(self, rule, link):
    #     r = scrapy.Request(url=link.url, callback=self._response_downloaded, headers=self.headers)
    #     r.meta.update(rule=rule, link_text=link.text)
    #     return r

    def parse_job(self, response):
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css('title', '.job-name::attr(title)')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        """
        下面这个得到的是公作要求相关的值，分别是salary，job_city，work_years，degree_need，job_type
        ['15k-30k ', '/北京 /', '经验3-5年 /', '本科及以上 /', '全职']
        """
        # job_request = response.css('.job_request p span::text').extract()
        # item_loader.add_value('salary', job_request[0].strip(' '))
        # item_loader.add_value('job_city', job_request[1].strip('/').strip(' '))
        # item_loader.add_value('work_years', job_request[2].strip('/').strip(' '))
        # item_loader.add_value('degree_need', job_request[3].strip('/').strip(' '))
        # item_loader.add_value('job_type', job_request[4].strip('/').strip(' '))
        # 这部分可以按上面的这样写，但是为了方便修改，处理的逻辑最好都放到item_loader中去
        item_loader.add_xpath('salary', '//dd[@class="job_request"]/p/span[1]/text()')
        item_loader.add_xpath('job_city', '//dd[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath('work_years', '//dd[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath('degree_need', '//dd[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('job_type', '//dd[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css('publish_time', '.publish_time::text')
        tag_list = response.css('.position-label.clearfix li::text').extract()
        item_loader.add_value('tags', ','.join(tag_list))
        item_loader.add_css('job_advantage', '.job-advantage p::text')
        item_loader.add_css('job_desc', '.job_bt div')
        item_loader.add_css('job_addr', '.work_addr')
        item_loader.add_css('company_url', '.job_company dt a::attr(href)')
        item_loader.add_css('company_name', '.job_company dt a img::attr(alt)')
        item_loader.add_value('crawl_time', datetime.datetime.now())

        lagou_item = item_loader.load_item()

        return lagou_item
