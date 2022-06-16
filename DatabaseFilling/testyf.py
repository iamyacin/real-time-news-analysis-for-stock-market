# -*- coding: utf-8 -*-
from yfinance import Ticker
from pymongo import MongoClient
import pandas as pd

mongo = MongoClient("mongodb://yacin:123@tradingnewsanalysis-shard-00-00-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-01-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-02-nbwxw.mongodb.net:27017/StockNewsDBProd?ssl=true&replicaSet=TradingNewsAnalysis-shard-0&authSource=admin&retryWrites=true&w=majority")
db = mongo['StockNewsDBProd']
collection = db["SocietiesInfos"]

tickers = pd.read_csv("Data/GeneratedData/tickers.csv")
tickersSymbol = tickers.tickerSymbol.to_list()

keys_cleaned = ["city", "country", "currency", "enterpriseValue", "extchange", "extchangeTimezoneName",
                "fax", "floatShares", "forwardEps", "forwardPE", "fullTimeEmployees", "industry",
                "logo_url", "longBusinessSummary", "longName", "marketCap", "payoutRatio", "pegRatio",
                "phone", "quoteType", "sector", "shortName", "state", "symbol", "trailingEps", 
                "trailingPE", "volume", "website"]

for ticker in tickersSymbol:
    try:
        cleaned_info = {}
        infos = Ticker(ticker).get_info()
        for key in keys_cleaned:
            cleaned_info[key] = infos.get(key)
        collection.insert_one(cleaned_info)
        print(f'Insert Done For {ticker}')
    except:
        print("infos no exist")
    
    

