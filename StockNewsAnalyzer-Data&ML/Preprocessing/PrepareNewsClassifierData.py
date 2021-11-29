# Sport == 0 -- world = 1 -- US == 2 -- business == 3 -- health == 4 -- entertainment == 5
# sci-thec ==6

import pandas as pd

#Importation des fichiers 
news_df = pd.read_csv('../Data/OtherNews.csv')
business_news_df = pd.read_csv('../Data/GeneratedData/LabeledNews.csv')

news_df = news_df.iloc[:,1:]

# La division des actualités sur deux segments businessNews et NonBusinessNews
other_news = news_df['data'][(news_df['flag'] == 0)
                     | (news_df['flag'] == 4) 
                     | (news_df['flag'] ==  5) 
                     | (news_df['flag'] ==  1) 
                     | (news_df['flag'] ==  2)].to_frame()
other_news['Class'] = 0

business_news = news_df['data'][(news_df['flag'] == 3) | (news_df['flag'] == 6)]

sample_news_from_business_news_df = business_news_df.News.sample(685)

business_news = business_news.append(sample_news_from_business_news_df).to_frame()
business_news['Class'] = 1

del news_df
del business_news_df
del sample_news_from_business_news_df

# la creation et le sauvegarde du nouveau fichier
other_news.columns = ['News', 'Class'] 
business_news.columns = ['News', 'Class']

news = other_news.append(business_news)

del other_news
del business_news

news = news.sample(frac=1).reset_index(drop=True)

news.to_csv('../Data/GeneratedData/NewsClasses(Other=0, Buissness=1).csv', index=False)

