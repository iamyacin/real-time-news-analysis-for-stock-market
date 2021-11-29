# -*- coding: utf-8 -*-
from newsapi import NewsApiClient
from pymongo import MongoClient


api = NewsApiClient(api_key="25704fb78efb48f8a6da73711b8f039f")

mongo = MongoClient("mongodb://yacin:123@tradingnewsanalysis-shard-00-00-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-01-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-02-nbwxw.mongodb.net:27017/StockNewsDBProd?ssl=true&replicaSet=TradingNewsAnalysis-shard-0&authSource=admin&retryWrites=true&w=majority")
db = mongo['StockNewsDBProd']
sourcesCollection = db["SourcesCollection"]

sourcesb = api.get_sources(language='en', country='us', category='business')
sourcest = api.get_sources(language='en', country='us', category='technology')
sourcesg = api.get_sources(language='en', country='us', category='general')

sourcesb = sourcesb['sources']
sourcest = sourcest['sources']
sourcesg = sourcesg['sources']

sources = sourcesb + sourcesg + sourcest

del sourcesb, sourcesg, sourcest

for source in sources:
    sourcesCollection.insert_one(source)
    print('insertion is okay !')
    

