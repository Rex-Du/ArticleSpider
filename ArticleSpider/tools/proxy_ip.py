# AuthorName : DuQing
# CreateTime : 2017-10-16 14:36
import random

import requests
from urllib import parse
import time

import MySQLdb

from scrapy.selector import Selector

headers = {
    'Host':'www.xicidaili.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit'
                    '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core'
                    '/1.53.3408.400 QQBrowser/9.6.12028.400'
}
# proxies = {
#     'http': 'http://120.78.15.63:80',
# }

conn = MySQLdb.connect('127.0.0.1', 'root', 'rootroot', 'article_spider',charset='utf8', use_unicode=True)
cursor = conn.cursor()


def parse_url(url):
    res = requests.get(url, headers=headers)
    selector = Selector(text=res.text)
    tr_list = selector.css('#ip_list tr')
    ip_list = []
    for tr in tr_list[1:]:
        ip_info = tr.css('td::text').extract()
        ip_addr = ip_info[0]
        port = ip_info[1]
        proxy_type = ip_info[5]
        ip_list.append((ip_addr, port, proxy_type))
    for ip in ip_list:
        cursor.execute(
            "insert into proxy_ip(ip_addr, port, proxy_type) VALUES ('{0}', '{1}', '{2}') ON DUPLICATE KEY UPDATE "
            "port=VALUES(port)".format(ip[0], ip[1], ip[2])

        )
        print(ip[0], ip[1], ip[2])
        conn.commit()


def delete_ip(ip):
    delete_sql = "delete from proxy_ip where ip_addr='{0}'".format(ip)
    cursor.execute(delete_sql)
    conn.commit()
    return True


def update_ip(ip):
    # 设置一个标识位，用于标记代理ip是否有效，如果有效下次就不再测试是否有效了
    update_sql = "update proxy_ip set is_valid=1 where ip_addr='{0}'".format(ip)
    cursor.execute(update_sql)
    conn.commit()
    return True


class GetIp(object):
    def judge_ip(self, ip, port, proxy_type):
        # 判断代理ip是否可用，不可用则删除
        http_url = 'http://www.baidu.com'
        proxy_url = proxy_type.lower() + '://' + ip + ':'+ port
        try:
            proxies = {
                proxy_type.lower():proxy_url,
            }
            res = requests.get(http_url, proxies=proxies)
        except Exception as e:
            print('Invalid ip and port! %s\n'%(ip))
            delete_ip(ip)
            return False
        else:
            code = res.status_code
            if code >=200 and code <300:
                update_ip(ip)
                print('Effective ip! %s\n'%(ip))
                return True
            else:
                print('Invalid ip and port! %s\n'%(ip))
                delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机取一条ip信息
        random_sql = """
                select ip_addr,port,proxy_type,is_valid from proxy_ip
                order by rand()
                limit 1
        """
        result = cursor.execute(random_sql)
        for ip in cursor.fetchall():
            ip_addr = ip[0]
            port = ip[1]
            proxy_type = ip[2]
            is_valid = ip[3]
            if not is_valid:
                is_valid = self.judge_ip(ip_addr, port, proxy_type)
            if is_valid:
                return proxy_type.lower() + '://' + ip_addr + ':'+ port
            else:
                return self.get_random_ip()

if __name__ == '__main__':
    for i in range(1, 100):
        start_url = 'http://www.xicidaili.com/nn/{0}'.format(i)
        parse_url(start_url)
        time.sleep(random.randint(5, 10))
    # get_ip = GetIp()
    # x = get_ip.get_random_ip()
    # print(x)
