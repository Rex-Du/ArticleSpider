# AuthorName : DuQing
# CreateTime : 2017-09-21 17:29
"""
因为pycharm不支持scrapy项目的调试，这里新建一个main文件，模拟命令行执行scrapy命令
"""
import sys
import os

from scrapy.cmdline import execute


sys.path.append(os.path.basename(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'jobbole'])
# execute(['scrapy', 'crawl', 'MonsterITCollege'])
# execute(['scrapy', 'crawl', 'zhihu'])
# execute(['scrapy', 'crawl', 'lagou'])
# execute(['scrapy', 'crawl', 'myspider'])
