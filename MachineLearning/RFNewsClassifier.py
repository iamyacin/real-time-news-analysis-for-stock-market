import pandas as pd
from nltk.stem.porter import PorterStemmer 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import RandomForestClassifier
import pickle
import dill

data = pd.read_csv('../Data/GeneratedData/NewsClasses(Other=0, Buissness=1).csv')

news = data.News.to_list()
Class = data.Class.to_list()

            
corpus = []
for inst in news:
    inst = inst.lower()
    inst = inst.split()
    ps = PorterStemmer()
    inst = [ps.stem(word) for word in inst if not word in set(stopwords.words('english'))]
    inst = ' '.join(inst)
    corpus.append(inst)
    
def text_transformer(txt):
    from nltk.stem.porter import PorterStemmer 
    from nltk.corpus import stopwords
    if isinstance(txt, str):
        txt = txt.lower()
        txt = txt.split()
        ps = PorterStemmer()
        txt = [ps.stem(word) for word in txt if not word in set(stopwords.words('english'))]
        txt = ' '.join(txt)
        return [txt]
    else:
        print("Enter a valide format (str) !")
            
vectorizer = CountVectorizer()
matrix_of_words = vectorizer.fit_transform(corpus).toarray()

selector = SelectKBest(chi2, k=900)
X = selector.fit_transform(matrix_of_words, Class)
    
X_train, X_test, y_train, y_test = train_test_split(X, Class, test_size = 0.20, random_state = 0)

classifier = RandomForestClassifier(n_estimators=100, random_state=111)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

cv = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

save_transformer = open("PythonObjects/NewsClassifierObjects/Transformer.pickle","wb")
dill.dump(text_transformer, save_transformer)
save_transformer.close()

save_vectorizer = open("PythonObjects/NewsClassifierObjects/Vectorizer.pickle","wb")
pickle.dump(vectorizer, save_vectorizer)
save_vectorizer.close()

save_selector = open("PythonObjects/NewsClassifierObjects/Selector.pickle","wb")
pickle.dump(selector, save_selector)
save_selector.close()

save_classifier = open("PythonObjects/NewsClassifierObjects/Classifier(RF).pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

t = dill.load(open("PythonObjects/NewsClassifierObjects/Transformer.pickle", "rb"))
v = pickle.load(open("PythonObjects/NewsClassifierObjects/Vectorizer.pickle", "rb"))
s = pickle.load(open("PythonObjects/NewsClassifierObjects/Selector.pickle", "rb"))
c = pickle.load(open("PythonObjects/NewsClassifierObjects/Classifier(RF).pickle", "rb"))

text = t("The solution to this problem is because input is just a String, but what is needed is a list (or an iterable) containing a single element (which is nothing but the String itself).")
vector = v.transform(text)
features = s.transform(vector)
prediction = c.predict(features)


