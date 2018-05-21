# AuthorName : DuQing
# CreateTime : 2017-09-25 11:00
import re
import json, time
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import requests
from requests import session


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/'
}
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookie.txt')


def get_xsrf():
    response = session.get('https://www.zhihu.com', headers=headers)
    _xsrf_regex = '[\s\S]*<input type="hidden" name="_xsrf" value="(.*?)"/>'
    res_xsrf = re.match(_xsrf_regex, response.text)
    if res_xsrf:
        _xsrf = res_xsrf.group(1)
    else:
        _xsrf = ''
    return _xsrf


def get_captcha():
    # 验证码URL是按照时间戳的方式命名的
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time() * 1000))
    response = session.get(captcha_url, headers=headers)
    # 保存验证码到当前目录
    with open('captcha.gif', 'wb') as f:
        f.write(response.content)
        f.close()

    # 自动打开刚获取的验证码
    from PIL import Image
    try:
        img = Image.open('captcha.gif')
        img.show()
        img.close()
    except:
        pass

    captcha = {
        'img_size': [200, 44],
        'input_points': [],
    }
    points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20], [129.796875, 22],
              [150.796875, 22]]
    print('7个字对应的坐标是：',points, '\n')
    seq = input('请输入倒立字的位置\n>')
    for i in seq:
        captcha['input_points'].append(points[int(i) - 1])
    return json.dumps(captcha)


def login_post(post_url, account, pwd):
    post_data = {
        '_xsrf': get_xsrf(),
        'password': pwd,
        'captcha_type': 'cn',
        'phone_num': account,
        'captcha': get_captcha(),
    }
    response_text = session.post(post_url, data=post_data, headers=headers)
    print(response_text.text)
    session.cookies.save()


def test_is_login():
    try:
        session.cookies.load()
    except:
        print('加载cookie失败')
    response = session.get('https://www.zhihu.com/inbox',headers=headers, allow_redirects = False)
    with open('sixin.html', 'wb') as f:
        f.write(response.text.encode('utf-8'))
        print('ok')

# post_url = 'https://www.zhihu.com/login/phone_num'
# login_post(post_url, '18627003837', 'duqing512556')
test_is_login()
