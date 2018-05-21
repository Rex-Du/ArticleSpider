# AuthorName : DuQing
# CreateTime : 2017-10-09 17:38
import hashlib
import re


def get_md5(url):
    if isinstance(url , str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    # 从字符串中提取出数字
    regex_str = '.*?(\d+).*'
    match_res = re.match(regex_str, text)
    if match_res:
        num = int(match_res.group(1))
    else:
        num = 0
    return num

if __name__ == '__main__':
    print(get_md5('http:\\www.baidu.com'))
