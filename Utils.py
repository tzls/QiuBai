# -*- coding:utf-8 -*-
from selenium import webdriver
import pymongo
import redis

class Utils(object):
    def __init__(self):
        pass
    def getDB(self,dbName):
        client = pymongo.MongoClient('localhost',27017)
        db =client[dbName]
        return db

    def getRedis(self):
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)
        return r

