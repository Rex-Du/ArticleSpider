# AuthorName : DuQing
# CreateTime : 2017-09-26 16:12
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36',
    'Host': 'fex.bdstatic.com',
    'Referer': 'https://tieba.baidu.com/index.html'
}
response = requests.get('https://tieba.baidu.com/index.html', headers=headers)
print(response.cookies)

