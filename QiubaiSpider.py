# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
from scrapy.selector import Selector
import json

class QiubaiSpider(object):
    def __init__(self):
        self.session = requests.session()
        header = {
            'Host': 'www.qiushibaike.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0'
        }
        response = self.session.get('https://www.qiushibaike.com/', headers=header)
        self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract_first()
        self.duration = Selector(response).xpath('//input[@name="duration"]/@value').extract_first()

    def login(self):
        header ={
            'Host':'www.qiushibaike.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0',

        }
        post_data={
            '_xsrf': self.xsrf,
            'duration': self.duration,
            'login': '彤在路上',
            'password': 'zhou123',
            'remember_me': 'checked'
        }
        #'{"user": {"login": "\\u5f64\\u5728\\u8def\\u4e0a", "unread_messages_count": 0, "id": 3465505, "avatar_file_name": "", "state": "active"}, "err": 0}'
        response = self.session.post('https://www.qiushibaike.com/new4/session',data=post_data,headers= header)
        response_json =json.loads(response.text)
        #print(response_json["user"]["login"].decode('unicode_escape'))
        try:
            if response_json["user"]["login"]:
                print("登录成功")
            else:
                print("登录失败")
        except:
            print("登录失败")

        
if __name__ =='__main__':
    qs = QiubaiSpider()
    qs.login()
