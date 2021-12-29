import pandas as pd
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB,GaussianNB,ComplementNB,BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


url='https://raw.githubusercontent.com/WebSec-ext/DataSet/main/sqli.csv.csv'
df=pd.read_csv(url,error_bad_lines=False,encoding='utf-8')

df = df.dropna(how='any',axis=0)

vectorizer = CountVectorizer( min_df=2, max_df=0.7, max_features=4096, stop_words=stopwords.words('english'))
#Learn the vocabulary dictionary and return document-term matrix.
posts = vectorizer.fit_transform(df['Sentence'].values.astype('U')).toarray()

#df.shape

posts.shape=(4189,64,64,1)

X=posts
Y=df['Label']

#Split arrays or matrices into random train and test subsets
# split train test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

trainX=X_train.copy()
trainX.shape=(X_train.shape[0],trainX.shape[1]*trainX.shape[2])
testX=X_test.copy()
testX.shape=(testX.shape[0],testX.shape[1]*testX.shape[2])


#saving the models
import pickle
def save(vectorizer, classifier,name):
    '''
    save classifier to disk
    '''
    n = name+".pkl"
    with open(n, 'wb') as file:
        pickle.dump((vectorizer, classifier), file)

#load the model
def load(name):
    '''
    load classifier from disk
    '''
    with open(name, 'rb') as file:
      vectorizer, classifier = pickle.load(file)
    return vectorizer, classifier


print("===============================================================")
print("Naive Bayes")
print("===============================================================")
gnb = GaussianNB()
classifierGNB = gnb.fit(trainX, Y_train)
#Perform classification on an array of test vectors X.
predGNB = gnb.predict(testX)
accuracyGNB = accuracy_score(Y_test,predGNB)
print("Accuracy:",accuracyGNB)
save(vectorizer, classifierGNB,"SQLiNaiveModel")
vectorizer, classiferNaive = load("SQLiNaiveModel.pkl")

#inp = ["An intent filter is an expression in an app's manifest file that specifies the type of intents that the component would like to receive."]
#inp = ["or 1 = 1 --"]
inp=["/random/folder/path.html?user='ajin'or '1' = '1' --"]
input_transformed = vectorizer.transform(inp)
predictionNaive = classiferNaive.predict(input_transformed.toarray())
print('Input:', inp)
print(predictionNaive)
if predictionNaive:
  print("SQLi")
else:
  print("Not SQLi")
print('The input is', 'SQLi' if predictionNaive else 'Not SQLi')


print("===============================================================")
print("Logistic Regression")
print("===============================================================")
logReg = LogisticRegression(solver='liblinear',C=10.0, random_state=0)
classifierLogReg = logReg.fit(trainX, Y_train)
#Perform classification on an array of test vectors X.
predLogReg = logReg.predict(testX)
accuracyLogReg = accuracy_score(Y_test,predLogReg)
print("Accuracy:",accuracyLogReg)

save(vectorizer, classifierLogReg,"SQLiLogisticRegModel")
vectorizer, classiferLog = load("SQLiLogisticRegModel.pkl")
                   
#inp = ["An intent filter is an expression in an app's manifest file that specifies the type of intents that the component would like to receive."]
inp = ["/random/folder/path.html?user='ajin'or '1' = '1' --"]
input_transformed = vectorizer.transform(inp)
predictionLog = classiferLog.predict(input_transformed.toarray())
print('Input:', inp)
print(predictionLog)
if predictionLog:
  print("SQLi")
else:
  print("Not SQLi")
print('The input is', 'SQLi' if predictionLog else 'Not SQLi')


print("===============================================================")
print("Decision Tree")
print("===============================================================")
from sklearn import tree
dt = tree.DecisionTreeClassifier()
classiferDT = dt.fit(trainX, Y_train)
predDT = classiferDT.predict(testX)
accuracyDT = accuracy_score(Y_test,predDT)
print("Accuracy:",accuracyDT)

save(vectorizer, classiferDT,"SQLiDTModel")
vectorizer, classiferDecisionTree = load("SQLiDTModel.pkl")

#inp = ["An intent filter is an expression in an app's manifest file that specifies the type of intents that the component would like to receive."]
#inp = ["or 1 = 1 --"]
inp=["/random/folder/path.html?user='ajin'or '1' = '1' --"]
input_transformed = vectorizer.transform(inp)
predictionDT = classiferDecisionTree.predict(input_transformed.toarray())
print('Input:', inp)
print(predictionDT)
if predictionDT:
  print("SQLi")
else:
  print("Not SQLi")
print('The input is', 'SQLi' if predictionDT else 'Not SQLi')
