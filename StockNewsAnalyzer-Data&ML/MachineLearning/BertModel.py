import ktrain
import pandas as pd
from ktrain import text
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


json_data = pd.read_json('../Data/LabeledData.json')

json_data = json_data.sample(frac=1).reset_index(drop=True)

df =  pd.DataFrame(json_data.iloc[:,0].to_list())

# Negative == 0 Neutral == 1 Positive == 2
sentiment = df.sentiment
encoder = LabelEncoder()
sentiment = encoder.fit_transform(sentiment)

txt = [df.title[i]+' '+df.text[i] for i in range(len(df))]

X_train, X_test, y_train, y_test = train_test_split(txt, sentiment, test_size = 0.15, random_state = 0)

(x_train,  y_train), (x_test, y_test), preproc = text.texts_from_array(x_train=X_train, y_train=y_train,
                                                                       x_test=X_test, y_test=y_test,
                                                                       class_names=[0,1,2],
                                                                       preprocess_mode='bert')

model = text.text_classifier(name = 'bert', train_data=(x_train, y_train), preproc=preproc)
learner = ktrain.get_learner(model, train_data=(x_train, y_train), batch_size=6)

learner.fit_onecycle(2e-5, 4)

learner.validate(val_data=(x_test, y_test), class_names=["Negative", "Neutral", "Positive"])

predictor = ktrain.get_predictor(learner.model, preproc)
predictor.get_classes()

predictor.save('../PythonObjects/Bert_Classifier')

reloaded_predictor = ktrain.load_predictor('../PythonObjects/Bert_Classifier')
reloaded_predictor.predict("A number of companies in the United States have decided to shutter their retail outlets and scale back on business in cities most disrupted by the protests organized in the wake of George Floyd's death")

