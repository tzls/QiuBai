# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import  BeautifulSoup
import json
class HtmlParser(object):
    def __init__(self):
        pass

    def parse_article_urls(self,response):
        article_urls = set()
        soup =BeautifulSoup(response,'lxml')
        soup_hrefs=soup.find_all("a",class_='contentHerf')
        for soup_href in soup_hrefs:
            article_url = soup_href.attrs['href']
            article_urls.add(article_url)
        return article_urls

    def parse_article_content(self,response):
        soup = BeautifulSoup(response,'lxml')
        soup_content = soup.find('div',class_='content').get_text()
        soup_comments = soup.find_all('div',class_='replay')
        comments=[]
        for soup_comment in soup_comments:
            comment = {}
            comment_content = soup_comment.find("span",class_='body').get_text()
            comment_people = soup_comment.find('a',class_='userlogin').attrs['title']
            comment['评论人'] = comment_people
            comment['评论'] = comment_content
            comments.append(comment)
        js ={"帖子":soup_content,'评论':comments}
        article_json = json.loads(json.dumps(js,ensure_ascii=False))
        return article_json





