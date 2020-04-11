# -*- coding: utf-8 -*-

__author__ = 'kikoxxxi'

import requests
import random
import time
import json
import math
import re
from .util import Util
from . import settings
from lxml import html


class LgSpider:
    util = Util()
    user_agent = getattr(settings, "MY_USER_AGENT")

    def __init__(self, kd, city_no, city='全国'):
        self.city = city
        self.kd = kd
        self.city_no = city_no
        self.refer_url = "https://www.lagou.com/jobs/list_{}/{}?px=new".format(self.util.url_encode(self.kd),
                                                                               self.city_no)
        # self.start_url = "https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false"
        self.start_url = "https://www.lagou.com/jobs/positionAjax.json?px=new&city={}&needAddtionalResult=false".format(
            self.util.url_encode(self.city))

    def get_form_data(self, first, pn, sid=None):
        if first:
            return {'first': 'true', 'pn': str(pn), 'kd': self.kd}
        return {'first': 'false', 'pn': str(pn), 'kd': self.kd, 'sid': sid}

    def get_data(self, result, head, detail=None, show_id=None):
        data = []
        for position in result:
            item = []
            for key in head:
                if position.get(key, -1) == -1:
                    continue
                item.append(position[key])
            if detail:
                position_id = position['positionId']
                detail_url = "https://www.lagou.com/jobs/{}.html?show={}".format(position_id, show_id)
                detail_html = self.start_requests(detail_url=detail_url)
                item.append(self.parse_detail(detail_html))
            print(item)
            data.append(item)
        return data

    def start_requests(self, first=True, pn=1, sid=None, *, detail_url=None):
        headers = {"Referer": self.refer_url, "User-Agent": random.choice(self.user_agent)}
        session = requests.Session()
        session.get(self.refer_url, headers=headers)  # 用session对象发出get请求，请求首页获取cookies
        cookies = session.cookies  # 为此次获取的cookies
        time.sleep(3)
        if detail_url:
            response = session.get(detail_url, headers={"User-Agent": random.choice(self.user_agent)}, cookies=cookies)
        else:
            form_data = self.get_form_data(first, pn, sid)
            response = session.post(self.start_url, data=form_data, headers=headers, cookies=cookies, timeout=3)
        # 设置字符编码为网站真实编码
        response.encoding = response.apparent_encoding
        return response.text

    def parse(self, content, first=True):
        # 转换为dict
        content = json.loads(content)
        content = content["content"]
        show_id = content["showId"]
        total_count = content["positionResult"]["totalCount"]
        position_result = content["positionResult"]["result"]

        company_head = getattr(settings, 'COMPANY_CSV_HEAD')
        position_head = getattr(settings, 'POSITION_CSV_HEAD')

        print("company data:")
        company_data = self.get_data(position_result, company_head)
        print("position data:")
        position_data = self.get_data(position_result, position_head, "position", show_id)

        self.util.append_csv(getattr(settings, 'COMPANY_CSV_FILE_NAME'), company_data)
        self.util.append_csv(getattr(settings, 'POSITION_CSV_FILE_NAME'), position_data)

        total_page = math.ceil(total_count / 15)
        print("total count: {}     total page: {}".format(total_count, total_page))

        if not first:
            return

        for pn in range(2, total_page + 1):
            print('''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> page {} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                '''.format(pn))
            next_content = self.start_requests(False, pn, show_id)
            self.parse(next_content, False)

    def parse_detail(self, detail):
        etree = html.etree
        h = etree.HTML(detail)
        result = re.sub(u"[\n\r\t\s\u3000\xa0]", "", h.xpath("string(//dd[@class='job_bt'])"))
        return result
