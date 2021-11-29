from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import pandas as pd
import pickle
import dill
import json
import ktrain


tickers = pd.read_csv("../Data/stocks_cleaned.csv")

LIST_OF_TICKERS_SYMBOL = tickers.iloc[:,0].to_list()
LIST_OF_TICKERS_SYMBOL = ['$'+ticker for ticker in LIST_OF_TICKERS_SYMBOL]
LIST_OF_TICKERS_NAME = tickers.iloc[:,1].to_list()
LIST_OF_TICKERS_NAME = [ticker.lower() for ticker in LIST_OF_TICKERS_NAME]

KEY = "zctpzZjqmeCMHubArCrsM45yU"
SECRET_KEY = "aR2dNMO3f5J9pgYvKAt5MPqb4ucDYiVYxGKW8ltYxqzTLCmFoB"
TOKEN = "1256257087694405633-BGfZWX31iFrUKXKgS4E5p7F4qwVwYX"
SECRET_TOKEN = "05i056h63TGERayKn44KKGW5mWJpeaVqMqPY05Zo0aaxL"

mongo = MongoClient("mongodb://yacin:123@tradingnewsanalysis-shard-00-00-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-01-nbwxw.mongodb.net:27017,tradingnewsanalysis-shard-00-02-nbwxw.mongodb.net:27017/StockNewsDBTest?ssl=true&replicaSet=TradingNewsAnalysis-shard-0&authSource=admin&retryWrites=true&w=majority")
db = mongo['StockNewsDBTest']
collection = db["NewsCollection"]

T = dill.load(open("../PythonObjects/NewsClassifierObjects/Transformer.pickle", "rb"))
V = pickle.load(open("../PythonObjects/NewsClassifierObjects/Vectorizer.pickle", "rb"))
S = pickle.load(open("../PythonObjects/NewsClassifierObjects/Selector.pickle", "rb"))
C = pickle.load(open("../PythonObjects/NewsClassifierObjects/Classifier(RF).pickle", "rb"))

ACCOUNTS_TO_FOLLOW = {'CNNMoneyEcon':'1354352203', 'TechCrunch':'816653', 'Benzinga':'44060322',
                      'MarketWatch':'624413', 'CNBC':'20402945', 'CNNBusiness':'16184358',
                      'geekwire':'255784266', 'InvezzPortal':'531415099', 'SeekingAlpha':'23059499',
                      'YahooFinance':'19546277', 'ReutersBiz':'15110357', 'greatquarter':'3369190451', 
                      '4xInsight':'266082837', 'Fxhedgers':'31064165', 'LiveSquawk':'59393368', 'DeItaOne':'2704294333',
                      'wsjbusiness':'28140646', 'business':'34713362', 'skynewsbiz':'113050195'}

classifier = ktrain.load_predictor('../PythonObjects/Bert_Classifier')

class Listener(StreamListener):
    
    def on_data(self, raw_data):
        post = self.process_data(raw_data)
        if post != 0:    
            self.store_data(post)
        return True  
    
    def process_data(self, raw_data):
        try:
            data = json.loads(raw_data)
            clas = C.predict(S.transform(V.transform(T(data['text']))))
            if int(clas)==1:
                #if not 'RT @' in data['text']:
                    tweetWords = data["text"].upper()
                    tweetWords = data["text"].split()
                    tickers = [ticker for ticker in LIST_OF_TICKERS_SYMBOL 
                               if ticker in tweetWords]
                    if len(tickers)!=0:
                        date = data["created_at"]
                        tweet = data["text"]
                        source = data["user"]["screen_name"]
                        prediction = classifier.predict(tweet)
                        post = {"DateTime": date, "source": source, "text": tweet, 
                                "ticker": tickers, "prediction": prediction}
                        return post
                    else:
                        print("This tweet not containe any ticker")
                        return 0
                #else:
                 #   print("This is a retweeted tweet")
                  #  return 0
            else:
                print("This tweet isn't a business news !")
                return 0
        except Exception as e : 
            print("Error on data : ",e.args)
            return 0
            
    def store_data(self, post):
        try:
            collection.insert_one(post)
            print("insertion Successed !")
        except Exception as e:
            print("Error on insertion : ",e.args)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)
            
auth = OAuthHandler(KEY, SECRET_KEY)
auth.set_access_token(TOKEN, SECRET_TOKEN)
twitterStream = Stream(auth, Listener())
twitterStream.filter(languages=['en'],follow = list(ACCOUNTS_TO_FOLLOW.values()))

