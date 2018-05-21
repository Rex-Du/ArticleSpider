# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

from ArticleSpider.utils.common import extract_num
from ArticleSpider.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT


class ArticlespiderItem(scrapy.Item):
    # define the Field()s for your item here like:
    # name = scrapy.Field()()
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()      # 将url转换为md5值，md5具有长度一致，好保存的特点
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field()
    praise_num = scrapy.Field()
    fav_num = scrapy.Field()
    comment_num = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    insert ignore into jobbole_article(title,create_date,url,url_object_id,
                    front_img_url,front_img_path,praise_num,fav_num,comment_num,tags,content)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        values = (
            self['title'], self['create_date'],
            self['url'], self['url_object_id'],
            self['front_img_url'], self['front_img_path'],
            self['praise_num'], self['fav_num'],
            self['comment_num'], self['tags'], self['content'][:200]
        )
        return insert_sql, values


class ZhihuQuestionItem(scrapy.Item):
    # 知乎问题item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,
        comments_num,watch_user_num,click_num,crawl_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE content=VALUES(content),
        comments_num=VALUES(comments_num), answer_num=VALUES(answer_num), click_num=VALUES(click_num)
        """
        # 这里做这些处理是因为用itemloader得到的item的值都是list的，所以要做转换
        zhihu_id = self['zhihu_id'][0]
        topics = ','.join(self['topics'])
        url = self['url'][0]
        title = ''.join(self['title'])
        content = '\n'.join(self['content'])
        answer_num = extract_num(''.join(self['answer_num']))
        comments_num = extract_num(''.join(self['comments_num']))
        watch_user_num = extract_num(self['watch_user_num'][0])
        click_num = extract_num(self['watch_user_num'][1] if len(self['watch_user_num'])==2 else '0')
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        values = (zhihu_id,topics,url,title,content,answer_num,
        comments_num,watch_user_num,click_num,crawl_time)
        return insert_sql, values


class ZhihuAnserItem(scrapy.Item):
    # 知乎回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 后面的on duplicate是mysql的特有写法，用于当插入重复时更新数据
        insert_sql = """
        insert into zhihu_answer(zhihu_id,url,question_id,author_id,content,praise_num,comments_num,
        create_time,update_time,crawl_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(content),
        comments_num=VALUES(comments_num), praise_num=VALUES(praise_num), update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self['create_time']).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self['update_time']).strftime(SQL_DATETIME_FORMAT)

        values = (self['zhihu_id'],self['url'],self['question_id'],self['author_id'],self['content'],
                  self['praise_num'],self['comments_num'],create_time, update_time,
                  self['crawl_time'].strftime(SQL_DATETIME_FORMAT))
        return insert_sql, values


def remove_splash(value):
    # 去除字符串中带有的 / 和 空格
    return value.replace('/', '').replace(' ', '')


def handle_addr(value):
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip() != '查看地图']
    return ''.join(addr_list)


class LagouJobItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    publish_time = scrapy.Field()
    tags = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_addr)
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        # 后面的on duplicate是mysql的特有写法，用于当插入重复时更新数据
        insert_sql = """
        insert into lagou_job(url, url_object_id, title, salary, job_city, work_years, degree_need, job_type, 
        publish_time, tags, job_advantage, job_desc, job_addr, company_url, company_name, crawl_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title),
        salary=VALUES(salary), publish_time=VALUES(publish_time), job_desc=VALUES(job_desc)
        """

        values = (self['url'], self['url_object_id'], self['title'], self['salary'], self['job_city'],
                  self['work_years'], self['degree_need'], self['job_type'], self['publish_time'], self['tags'],
                  self['job_advantage'], self['job_desc'], self['job_addr'], self['company_url'],
                  self['company_name'], self['crawl_time'].strftime(SQL_DATETIME_FORMAT))
        return insert_sql, values


class LagouJobItemLoader(ItemLoader):
    # 自定义了ItemLoader，这样做的原因是自带的ItemLoader得到的字段是列表，重写了下面的参数得到的字段就是字符串了
    default_output_processor = TakeFirst()

