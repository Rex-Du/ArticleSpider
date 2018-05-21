# -*- coding: utf-8 -*-
import json, re, time, datetime
from urllib import parse

import scrapy
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnserItem, ZhihuQuestionItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com/']
    start_urls = ['https://www.zhihu.com/']

    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        "authorization": "Bearer Mi4xdVRvSUJnQUFBQUFBY01JeFJ5TnVEQmNBQUFCaEFsVk4yeUQwV1FDYlF0akhIZEhUTlk4T1NiSVVNRk9KbzNTYmdR|1506579419|13eece09d3179438af41b8f8e0fef932734d9923",
    }
    # 下面这个是使用自己的setting，而不用settings.py文件中的setting
    custom_settings = {
        'COOKIES_ENABLED': True
    }

    def parse(self, response):
        all_urls = response.xpath('//a/@href').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        for url in all_urls:
            print(url)
            match_obj = re.match('(.*www.zhihu.com/question/(\d+))', url)
            if match_obj:
                # 如果找到了question相关的页面，则下载后交由提取函数处理
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question, dont_filter=True)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', '.QuestionHeader h1.QuestionHeader-title::text')
        item_loader.add_css('content', '.QuestionHeader-detail span')
        item_loader.add_value('url', response.url)

        match_obj = re.match('(.*www.zhihu.com/question/(\d+))', response.url)
        if match_obj:
            question_id = int(match_obj.group(2))
        item_loader.add_value('zhihu_id', question_id)
        item_loader.add_css('answer_num', 'h4.List-headerText span::text')
        item_loader.add_css('comments_num', '.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num', '.NumberBoard-value::text')
        item_loader.add_css('topics', '.QuestionHeader-topics .Popover div::text')

        question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer, dont_filter=True)
        yield question_item

    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json['paging']['is_end']
        total = ans_json['paging']['totals']
        next_url = ans_json['paging']['next']
        # 提取answer的具体字段
        for answer in ans_json['data']:
            answer_item = ZhihuAnserItem()
            answer_item['zhihu_id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['question_id'] = answer['question']['id']
            answer_item['author_id'] = answer['author']['id'] if 'id' in answer['author'] else ''
            answer_item['content'] = answer['content'] if 'content' in answer else ''
            answer_item['praise_num'] = answer['voteup_count']
            answer_item['comments_num'] = answer['comment_count']
            answer_item['create_time'] = answer['created_time']
            answer_item['update_time'] = answer['question']['updated_time']
            answer_item['crawl_time'] = datetime.datetime.now()

            yield answer_item
        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer,dont_filter=True)

    # 爬虫一开始执行的是下面这个方法，因为知乎要先登录才能访问，所以这里要重载这个方法
    def start_requests(self):
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time() * 1000))
        return [scrapy.Request(captcha_url, headers=self.headers, callback=self.get_captcha)]

    def get_captcha(self, response):
            with open('captcha.gif', 'wb') as f:
                f.write(response.body)
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
            points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20],
                      [129.796875, 22],
                      [150.796875, 22]]
            print('7个字对应的坐标是：', points, '\n')
            seq = input('请输入倒立字的位置\n>')
            for i in seq:
                captcha['input_points'].append(points[int(i) - 1])
            return [scrapy.Request(url='https://www.zhihu.com/', callback=self.login,meta={'captcha':json.dumps(captcha)},
                                   headers=self.headers, dont_filter=True)]

    def login(self, response):
        _xsrf_regex = '[\s\S]*<input type="hidden" name="_xsrf" value="(.*?)"/>'
        res_xsrf = re.match(_xsrf_regex, response.text)
        if res_xsrf:
            _xsrf = res_xsrf.group(1)
            print(_xsrf)
        else:
            _xsrf = ''
        if _xsrf:
            post_data = {
                '_xsrf': _xsrf,
                'password': 'duqing512556',
                'captcha_type': 'cn',
                'phone_num': '18627003837',
                'captcha': response.meta['captcha'],
            }
            post_url = 'https://www.zhihu.com/login/phone_num'
            return [scrapy.FormRequest(url=post_url,  formdata=post_data, headers=self.headers,
                                       callback=self.check_login, dont_filter=True)]

    def check_login(self, response):
        res_dict = json.loads(response.text)
        print(res_dict['msg'])
        if 'msg' in res_dict and res_dict['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers, callback=self.parse)

