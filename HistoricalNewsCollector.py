from newsapi import NewsApiClient
from pymongo import MongoClient
from ktrain import load_predictor
import pandas as pd
import config

            
api = NewsApiClient(api_key=config.API1)

api2 = NewsApiClient(api_key=config.API2)

classifier = load_predictor("PythonObjects/PolarityClassifier")

mongo = MongoClient(config.MONGO)
db = mongo[config.DB]
newsCollection = db[config.COLLECTION]

tickers = pd.read_csv("Data/stocks_cleaned.csv")
tickerSymbol = tickers.iloc[:,0].to_list()
tickerName = tickers.iloc[:,1].to_list()
tickerName = [item.replace(" ", "+") for item in tickerName]

for i in range(101, len(tickerName)):
    result = api2.get_everything(qintitle=tickerSymbol[i]+' OR '+tickerName[i], page_size=100,
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
                  