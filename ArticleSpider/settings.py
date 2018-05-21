# -*- coding: utf-8 -*-
import os
import sys
# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArticleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules     # 爬虫协议，会读取网站上的爬虫协议，过滤相关的url，设置为false就不会过滤了
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 8
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'ArticleSpider.middlewares.MyCustomDownloaderMiddleware': 543,
    # 禁用默认的UserAgentMiddleware，不禁用的话，会导致将默认的UserAgent都变成scrapy了
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'ArticleSpider.middlewares.RandomUserAgentMiddleware': 666,
    # 'ArticleSpider.middlewares.RandomIPProxyMiddleware': 665
    # 请求动态页面的中间件
    #  'ArticleSpider.middlewares.JSPageRequestMiddleware': 1
}

RANDOM_UA_TYPE = 'ie'
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
   #  'scrapy.pipelines.images.ImagesPipeline': 1,        # 添加图片自动下载的管道，后面的数字越小优先级越高
    # 'ArticleSpider.pipelines.ArticleImagePipline': 1,        # 得到front_img_path的管道
    # 'ArticleSpider.pipelines.MysqlPipline': 2,        # 保存到数据库，传统方法，受数据量的限制可能会产生堆积
    'ArticleSpider.pipelines.MysqlTwistedPipline': 2,        # 异步方法保存到数据库，大大提升入库的效率
}
IMAGES_URLS_FIELD = 'front_img_url'
project_path = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_path, 'images')

# 下面这几步操作是为了在几个py文件中相互导入时可以找到位置
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print(BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'ArticleSpider'))

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'rootroot'
MYSQL_DB = 'article_spider'
MYSQL_CHARSET = 'utf8'
MYSQL_USE_UNICODE = True

SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
SQL_DATE_FORMAT = '%Y-%m-%d'

# 禁止重定向，设置之后就不爬取重定向之后的页面，避免报错
REDIRECT_ENABLED = False