import pandas as pd
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB,GaussianNB,ComplementNB,BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import featureExtractionPhish
import numpy as np
#reading the dataset...
#url='https://raw.githubusercontent.com/WebSec-ext/DataSet/main/datasetCD.csv'

url='https://raw.githubusercontent.com/WebSec-ext/DataSet/main/PhishingDataSet.csv'
df=pd.read_csv(url,error_bad_lines=False,encoding='utf-8')

#df=pd.read_csv('PhishingDataSet.csv')

df = df.dropna(how='any',axis=0)


X=df.drop(['Result'],axis=1)
y=df['Result']


X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size = 0.2)


#saving the models
import pickle
def save(classifier,name):
    '''
    save classifier to disk
    '''
    n = name+".pkl"
    with open(n, 'wb') as file:
        pickle.dump(classifier, file)

#load the model
def load(name):
    '''
    load classifier from disk
    '''
    with open(name, 'rb') as file:
      classifier = pickle.load(file)
    return classifier


print("Perform Sample Tests...")
print("===============================================================")
print("Decisison Tree")
print("===============================================================")

from sklearn import tree
classifierDT = tree.DecisionTreeClassifier()
classifierDT = classifierDT.fit(X_train, Y_train)
pred_dt = classifierDT.predict(X_test)
accuracyDectr = accuracy_score(Y_test,pred_dt)
print("DT - Accuracy:",accuracyDectr)

save(classifierDT,"PhishingDTModel")
classiferDTsaved = load("PhishingDTModel.pkl")

url="https://www.iiitmk.ac.in/moodle/course/view.php?id=629"
X_input = url
#print("Url op1 : "+str(X_input))
X_new=featureExtractionPhish.generate_data_set(X_input)
X_new = np.array(X_new).reshape(1,-1)
#print("reshape op1 : "+str(X_new))

predictionDT = classiferDTsaved.predict(X_new)
print("prediction op : "+str(predictionDT))
if predictionDT == -1:
    print("Phishing Url")
else:
    print("Legitimate Url")


print("Perform Sample Tests...")
print("===============================================================")
print("Logistic Regression")
print("===============================================================")

classifierLR = LogisticRegression(solver='liblinear',C=10.0, random_state=0)
classifierLR = classifierLR.fit(X_train, Y_train)
predt_LR=classifierLR.predict(X_test)
accuracyLR = accuracy_score(Y_test,predt_LR)
print("LR - Accuracy:",accuracyLR)
save(classifierLR,"PhishingLRModel")
classiferLRsaved = load("PhishingLRModel.pkl")              

url="https://www.iiitmk.ac.in/moodle/course/view.php?id=629"
X_input = url
X_new=featureExtractionPhish.generate_data_set(X_input)
X_new = np.array(X_new).reshape(1,-1)

predictionLR = classiferLRsaved.predict(X_new)
print("prediction op : "+str(predictionLR))
if predictionLR == -1:
    print("Phishing Url")
else:
    print("Legitimate Url")
  

print("Perform Sample Tests...")
print("===============================================================")
print("Random Forest")
print("===============================================================")

modelRF = RandomForestClassifier()
modelRF = modelRF.fit(X_train, Y_train)
predt_RF = modelRF.predict(X_test)
accuracyRF = accuracy_score(Y_test,predt_RF)
print("RF - Accuracy:",accuracyRF)
save(modelRF,"PhishingRFModel")
classiferRFsaved = load("PhishingRFModel.pkl")                 

url="https://www.iiitmk.ac.in/moodle/course/view.php?id=629"
X_input = url
X_new=featureExtractionPhish.generate_data_set(X_input)
X_new = np.array(X_new).reshape(1,-1)

predictionRF = classiferRFsaved.predict(X_new)
print("prediction op : "+str(predictionRF))
if predictionRF == -1:
    print("Phishing Url")
else:
    print("Legitimate Url")

