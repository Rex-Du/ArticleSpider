# -*- coding: utf-8 -*-
import re
import datetime

import scrapy
from scrapy.http import Request

from ArticleSpider.items import ArticlespiderItem
from ArticleSpider.utils.common import get_md5
from settings import IMAGES_STORE


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    # start_urls = ['http://flights.ctrip.com/booking/SHA-CAN-day-1.html?DDate1=2017-11-07#DDate1=2017-11-07']

    def parse(self, response):
        """
        1、获取到当前页的所有文章url并交给parse_detail函数去解析
        2、得到下一页的url，并交给parse继续爬取
        """
        article_nodes = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
        for node in article_nodes:
            url = node.xpath('@href').extract_first()
            front_img_url = node.xpath('img/@src').extract_first()
            yield Request(url=url, callback=self.parse_detail, meta={'img_url': front_img_url})

        next_page_url = response.xpath('//*[@id="archive"]//a[@class="next page-numbers"]/@href').extract_first()
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse)

    def parse_detail(self, response):
        front_img_url = response.meta.get('img_url', '')
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_date =  response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·','').strip()
        praise_num = int( response.xpath('//h10/text()').extract_first())
        # 收藏数文字串，如：39收藏
        fav_str = response.xpath('//div[@class="post-adds"]//span[contains(@class,"bookmark-btn")]/text()').extract_first().strip()
        fav_regex_str = '.*?(\d+).*'
        fav_match_res =  re.match(fav_regex_str, fav_str)
        if fav_match_res:
            fav_num = fav_match_res.group(1)
        else:
            fav_num = 0
        # 评论数的文字串，如：890评论
        comment_str = response.xpath('//a[@href="#article-comment"]/span[contains(@class,"href-style")]/text()').extract_first().strip()
        comment_regex_str = '.*?(\d+).*'
        comment_match_res = re.match(comment_regex_str, comment_str)
        if comment_match_res:
            comment_num = comment_match_res.group(1)
        else:
            comment_num = 0
        tags_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()     # 结果是列表，如 ['IT技术', '开发']
        tags = ','.join(tags_list)
        content = '\n'.join(response.xpath('//div[@class="entry"]/p/text()').extract())       # 结果是列表，如 ['IT技术', '开发']

        try:
            create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.date()
        article_item = ArticlespiderItem()
        article_item['title'] = title
        article_item['create_date'] = create_date
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['front_img_url'] = [front_img_url]
        article_item['front_img_path'] = [IMAGES_STORE]
        article_item['praise_num'] = praise_num
        article_item['fav_num'] = fav_num
        article_item['comment_num'] = comment_num
        article_item['tags'] = tags
        article_item['content'] = content

        yield article_item

