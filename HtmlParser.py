# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import  BeautifulSoup
class HtmlParser(object):
    def __init__(self):
        pass

    def parse_article_urls(self,response):
        article_urls = set()
        soup =BeautifulSoup(response,'lxml')
        soup_hrefs=soup.find_all("a",class_='contentHerf')
        for soup_href in soup_hrefs:
            article_url = soup_href.attrs['href']
            article_urls.append(article_url)
        return article_urls




