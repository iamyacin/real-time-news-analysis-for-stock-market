# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 01:18:59 2020

@author: Yaçin
"""

import pandas as pd

#Faire des transformations aux niveau du fichier des tickers
tickers = pd.read_csv("../Data/stocks_cleaned.csv")
tickerSymbol = tickers.iloc[:,0].to_list()
strTickerSympol = ','.join(tickerSymbol)
tickerName = tickers.iloc[:,1].to_list()
tickerName = [item.replace(" ", "+") for item in tickerName]

from newsapi import NewsApiClient

api = NewsApiClient(api_key="25704fb78efb48f8a6da73711b8f039f")

#Faire un filtre pour garder juste les tickers qui ont plus de 10 actualités ce mois  
tickers_to_get = []
for i in range(500, len(tickerSymbol)):
    result = api.get_everything(qintitle=tickerSymbol[i]+' OR '+tickerName[i], 
                                 sort_by='popularity', language='en')
    result = result['articles']
    if len(result) > 10:
        print(f'Okay, for {tickerSymbol[i]}')
        tickers_to_get.append(tickerSymbol[i])
    else :
        print(f'No, for {tickerSymbol[i]}')
        
# La creation du nouveau fichier et le sauvegarder forma csv        
new_tickers_file=[{'tickerName':tickers[' name'][i],'tickerSymbol': tickers['ticker'][i]} 
                    for i in range(len(tickers)) 
                    if tickers['ticker'][i] in tickers_to_get]

tickers_df = pd.DataFrame(new_tickers_file)

tickers_df.to_csv('../Data/GeneratedData/tickers.csv', index=False)












