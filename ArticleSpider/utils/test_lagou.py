# AuthorName : DuQing
# CreateTime : 2017-10-12 16:33
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400',
    'Host': 'www.lagou.com',
    'Upgrade-Insecure-Requests': '1'
}
response = requests.get('https://www.lagou.com', headers=headers)
print(response.content.decode())


