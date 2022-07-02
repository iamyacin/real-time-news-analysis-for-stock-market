from ast import Import
from distutils.command.config import config
from newsapi import NewsApiClient
from pymongo import MongoClient
from ktrain import load_predictor
import datetime as dt
import pandas as pd
from time import sleep
import config


classifier = load_predictor('../PythonObjects/Bert_Classifier')

mongo = MongoClient("mongodb://yacin:123@tradingnewsanalysis-shard-00-00-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-01-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-02-nbwxw.mongodb.net:27017/StockNewsDBProd?ssl=true&replicaSet=TradingNewsAnalysis-shard-0&authSource=admin&retryWrites=true&w=majority")
db = mongo['StockNewsDBProd']
newsCollection = db['NewsCollection']
test = db['test']

tickers = pd.read_csv("../Data/GeneratedData/tickers.csv")
tickerName = tickers.iloc[:,0].to_list()
tickerSymbol = tickers.iloc[:,1].to_list()
tickerName = [item.replace(" ", "+") for item in tickerName]

def getNews(firstApi = None, secondApi = None, tickerSymbol = tickerSymbol, tickerName = tickerName):
    news = []
    current_datetime = dt.datetime.now().replace(microsecond=0)
    datetime_toUse = current_datetime - dt.timedelta(hours=2, minutes=30)
    datetime_toUse = str(datetime_toUse).replace(" ","T")
    for i in range(0, 200):
        try:
            result = firstApi.get_everything(qintitle=tickerSymbol[i]+' OR '+tickerName[i], page_size=100, 
                                             from_param=datetime_toUse, sort_by='popularity', language='en')
            result = result['articles']
            [item.pop("content") for item in result]
            [item.update({'prediction' : classifier.predict(item['title']+' '+item['description'])}) for item in result if item['description'] is not None and item['title'] is not None]
            [item.update({'ticker' : '$'+tickerSymbol[i]}) for item in result]
            posts = [item for item in result if len(item)> 8]
            [news.append(item) for item in posts if len(posts) != 0]
            print(f"Done, for {tickers['tickerName'][i]}")
        except Exception as e: 
            print('Error : '+ str(e))
            
    for i in range(200, len(tickers)):
        try:
            result = secondApi.get_everything(qintitle=tickerSymbol[i]+' OR '+tickerName[i], page_size=100, 
                                              from_param=datetime_toUse, sort_by='popularity', language='en')
            result = result['articles']
            [item.pop("content") for item in result]
            [item.update({'prediction' : classifier.predict(item['title']+' '+item['description'])}) for item in result if item['description'] is not None and item['title'] is not None]
            [item.update({'ticker' : '$'+tickerSymbol[i]}) for item in result]
            posts = [item for item in result if len(item)> 8]
            [news.append(item) for item in posts if len(posts) != 0]
            print(f"Done, for {tickers['tickerName'][i]}")
        except Exception as e:
            print('Error : '+ str(e))
    
    return news

def newsInsertion(news = None):
    try:
        for item in news:
            newsCollection.insert_one(item)
        print(f"Insertion is Done")
    except Exception as e:
        print('Error on Insertion : '+ str(e))

while True:
    news = getNews(firstApi=NewsApiClient(api_key=config.API1), secondApi=NewsApiClient(api_key=config.API2))
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=NewsApiClient(api_key=config.API3), secondApi=NewsApiClient(api_key=config.API4))
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=NewsApiClient(api_key=config.API5), secondApi=NewsApiClient(api_key=config.API6))
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=NewsApiClient(api_key=config.API7), secondApi=NewsApiClient(api_key=config.API8))
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=NewsApiClient(api_key=config.API9), secondApi=NewsApiClient(api_key=config.API10))
    newsInsertion(news=news)
    sleep(9000)