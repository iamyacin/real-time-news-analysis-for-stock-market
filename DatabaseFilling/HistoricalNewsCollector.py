from newsapi import NewsApiClient
from pymongo import MongoClient
from ktrain import load_predictor
import pandas as pd

            
api = NewsApiClient(api_key="25704fb78efb48f8a6da73711b8f039f")

api2 = NewsApiClient(api_key="34931c1e7de3477ab3ed7eede23be27a")

classifier = load_predictor('../PythonObjects/Bert_Classifier')

mongo = MongoClient("mongodb://yacin:123@tradingnewsanalysis-shard-00-00-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-01-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-02-nbwxw.mongodb.net:27017/StockNewsDBProd?ssl=true&replicaSet=TradingNewsAnalysis-shard-0&authSource=admin&retryWrites=true&w=majority")
db = mongo['StockNewsDBProd']
newsCollection = db['NewsCollection']

tickers = pd.read_csv("Data/stocks_cleaned.csv")
tickerSymbol = tickers.iloc[:,0].to_list()
tickerName = tickers.iloc[:,1].to_list()
tickerName = [item.replace(" ", "+") for item in tickerName]

for i in range(0, len(tickerName)):
    result = api.get_everything(qintitle=tickerSymbol[i]+' OR '+tickerName[i], page_size=100,
                                 sort_by='popularity', language='en')
    result = result['articles']
    [item.pop("content") for item in result]
    [item.update({'prediction' : classifier.predict(item['title']+' '+item['description'])}) for item in result if item['description'] is not None and item['title'] is not None]
    [item.update({'ticker' : '$'+tickerSymbol[i]}) for item in result]
    posts = [item for item in result if len(item)> 8]
    if len(posts) != 0:
        for item in posts:
            newsCollection.insert_one(item)
        print(f'Okay, for {tickerSymbol[i]}')
    else:
        print(f'Nothing to insert for {tickerName[i]}')
                  