import pandas as pd

json_data = pd.read_json('../Data/CollectedData/LabeledData.json')

df =  pd.DataFrame(json_data.iloc[:,0].to_list())

df = df.sample(frac=1).reset_index(drop=True)

df_majorityPos = df[df.sentiment == "Positive"]
df_majorityNeu = df[df.sentiment == "Neutral"]
df_minority = df[df.sentiment == "Negative"]

df_pos = df_majorityPos.sample(len(df_minority))
df_Neu = df_majorityNeu.sample(len(df_minority))

balanced_df = pd.concat([df_minority, df_pos, df_Neu], axis=0)

del json_data
del df
del df_majorityNeu
del df_majorityPos
del df_minority
del df_Neu
del df_pos

balanced_df = balanced_df.sample(frac=1).reset_index(drop=True)

balanced_df.to_csv('../Data/GeneratedData/BalencedLabeledNews.csv', index=False)

sentiment = balanced_df.sentiment

news = [balanced_df.title[i]+' '+balanced_df.text[i] for i in range(len(balanced_df))]

labledNews = pd.DataFrame({'News':news, 'Sentiment':sentiment})

del news
del sentiment

labledNews.to_csv('../Data/GeneratedData/LabeledNews.csv', index=False)