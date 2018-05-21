# AuthorName : DuQing
# CreateTime : 2017-09-22 16:44
import re
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
              '53.0.2785.104 Safari/537.36 Core/1.53.3387.400 QQBrowser/9.6.11984.400',
    'Host': 'passport.jd.com',
    'Referer': 'https://passport.jd.com/new/login.aspx'
}


def index_get():
    response = requests.get('https://passport.jd.com/new/login.aspx', headers=headers)
    print(response.text)


def get_post_data(account):
    response = requests.get('https://passport.jd.com/new/login.aspx', headers=headers)
    uuid_regex = '[\s\S]*id="uuid" name="uuid" value="(.*?)"'  # 这里最前面必需用\s\S，这样才能匹配所有字符，.并不能匹配任意字符
    eid_regex = '[\s\S]*id="eid" value="(.*?)" class="hide"/>'
    fp_regex = '[\s\S]*name="fp" id="sessionId" value="(.*?)" class="hide"'
    _t_regex = '[\s\S]*name="_t" id="token" value="(.*?)" class="hide"/>'
    loginType_regex = '[\s\S]*name="loginType" id="loginType" value="c" class="hide"/>'
    pubKey = '[\s\S]*name="pubKey" id="pubKey" value="(.*?)" class="hide"/>'

    res = re.match(uuid_regex, response.text)
    if res:
        uuid =res.group(1)
    else:
        uuid = ''
    print(uuid)


def login_post(account, pwd):
    uuid = ''
    post_url = 'https://passport.jd.com/uc/loginService?uuid={0}&version=2015'.format(uuid)
    post_data = {
    }


get_post_data()