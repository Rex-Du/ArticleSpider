# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
from MySQLdb import cursors
from twisted.enterprise import adbapi       # 这个api可以装mysql的操作变成异步的操作

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipline(ImagesPipeline):
    # 为了得到front_img_path的值，重写了ImagesPipeline类中下面的这个方法
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_img_path'] = image_file_path
        return item


class MysqlPipline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'rootroot', 'article_spider',
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title,create_date,url,url_object_id,
            front_img_url,front_img_path,praise_num,fav_num,comment_num,tags,content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        """
        values = (
            item['title'],item['create_date'],
            item['url'],item['url_object_id'],
            item['front_img_url'],item['front_img_path'],
            item['praise_num'],item['fav_num'],
            item['comment_num'],item['tags'],item['content']
        )
        self.cursor.execute(insert_sql, values)
        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            database = settings['MYSQL_DB'],
            charset = settings['MYSQL_CHARSET'],
            use_unicode = settings['MYSQL_USE_UNICODE']
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item)

    def handle_error(self, failure, item):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, values = item.get_insert_sql()      # 这种写法就要求每个item类里必需要有get_insert_sql这个方法
        cursor.execute(insert_sql, values)
