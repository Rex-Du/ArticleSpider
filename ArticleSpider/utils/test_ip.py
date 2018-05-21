# AuthorName : DuQing
# CreateTime : 2017-10-17 11:47
import requests

http_url = 'http://www.baidu.com'
try:
    proxies = {
       'https' : 'https://110.73.28.243:24908'
    }
    res = requests.get(http_url, proxies=proxies)
except Exception as e:
    print(e)
    print('Invalid ip and port! ')
else:
    code = res.status_code
    if code >=200 and code <300:
        print('Effective ip! ', code)
    else:
        print('Invalid ip and port! ')


