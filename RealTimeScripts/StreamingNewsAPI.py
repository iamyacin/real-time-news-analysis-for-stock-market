from newsapi import NewsApiClient
from pymongo import MongoClient
from ktrain import load_predictor
import datetime as dt
import pandas as pd
from time import sleep
            
api1 = NewsApiClient(api_key="25704fb78efb48f8a6da73711b8f039f")
api2 = NewsApiClient(api_key="34931c1e7de3477ab3ed7eede23be27a")
api3 = NewsApiClient(api_key="8bafac01575d4bf9849509503bd56766")
api4 = NewsApiClient(api_key="65cdbdd16e6d4fd5a98794a942432d4b")
api5 = NewsApiClient(api_key="1297735673f8474aa4b1b438b1596678")
api6 = NewsApiClient(api_key="2dc7c51836e1475a8ef94bbf74684671")
api7 = NewsApiClient(api_key="3ffe2d25c5f94296886d9c20c0011653")
api8 = NewsApiClient(api_key="d8024cbb353849efbfce1c57dfc8b5cc")
api9 = NewsApiClient(api_key="51936d9913634e5cafc87c24b8808aa5")
api10 = NewsApiClient(api_key="fc9a5b8c1ac14dfa847a068c1a21b7f0")

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
    news = getNews(firstApi=api1, secondApi=api2)
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=api3, secondApi=api4)
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=api5, secondApi=api6)
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=api7, secondApi=api8)
    newsInsertion(news=news)
    sleep(9000)
    
    news = getNews(firstApi=api9, secondApi=api10)
    newsInsertion(news=news)
    sleep(9000)