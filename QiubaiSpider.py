# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
from scrapy.selector import Selector
import json
from Utils import *
from HtmlParser import *
class QiubaiSpider(object):
    def __init__(self):
        self.session = requests.session()
        self.utils = Utils()
        self.redis = self.utils.getRedis()
        self.htmlparser = HtmlParser()
        self.db = self.utils.getDB('QiuBai')
        #new_topic_urls:未爬取的topic的URL
        #new_article_urls:未爬取的article的URL
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
        # topics = ['8hr','hot','imgrank','text','history']
        # for topic in topics:
        #     for index in range(1,14):
        #         page = '/%s/page/%s'%(topic,index)
        #         self.redis.sadd('new_topic_urls',page)
        #
        # while True:
        #     if self.redis.smembers('new_topic_urls'):
        #         topic_url_last = self.redis.spop('new_topic_urls')
        #         topic_url = 'http://www.qiushibaike.com%s'%(topic_url_last.decode())
        #         print('topic_url.........',topic_url)
        #         response = self.session.get(topic_url,headers = header)
        #         article_urls = self.htmlparser.parse_article_urls(response.text)
        #         for article_url in article_urls:
        #             self.redis.sadd('new_article_urls',article_url)
        #     else:
        #         print("爬取topic结束")
        #         break
        while True:
            if self.redis.smembers('new_article_urls'):
                article_url_last = self.redis.spop('new_article_urls')
                article_url ='http://www.qiushibaike.com%s'%(article_url_last.decode())
                print('article_url....',article_url)
                response = self.session.get(article_url,headers=header)
                article_json = self.htmlparser.parse_article_content(response.text)
                self.db.collections.insert(article_json)
            else:
                print('爬取结束')





        
if __name__ =='__main__':
    qs = QiubaiSpider()
    qs.login()
