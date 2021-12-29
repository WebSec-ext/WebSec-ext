import pandas as pd
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from sklearn.feature_extraction.text import CountVectorizer


s="https://book.hacktricks.xyz/pentesting-web/alert(document.cookie)/user=admin'or'1'='1'--"

url='https://raw.githubusercontent.com/WebSec-ext/DataSet/main/XSS_dataset.csv'
df=pd.read_csv(url,error_bad_lines=False,encoding='utf-8')
#Drop the empty lines
##print("Before : \n",df.count())
df = df.dropna(how='any',axis=0)
##print("After : \n",df.count())
#Convert a collection of text documents to a matrix of token counts
vectorizer = CountVectorizer( min_df=2, max_df=0.7, max_features=4096, stop_words=stopwords.words('english'))
#Learn the vocabulary dictionary and return document-term matrix.
posts = vectorizer.fit_transform(df['Sentence'].values.astype('U')).toarray()

#reshaping..
posts.shape=(13686,64,64,1)

X=posts
y=df['Label']

#Split arrays or matrices into random train and test subsets
from sklearn.model_selection import train_test_split

# split train test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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


print("Perform Sample Tests...")
print("===============================================================")
print("Support Vector Machine")
print("===============================================================")
# SVM
from sklearn.svm import SVC
classifierSVM = SVC(gamma='auto')
#Fit the SVM model according to the given training data.
classifierSVM = classifierSVM.fit(trainX, y_train)
#Perform classification on samples in X.
pred_svm=classifierSVM.predict(testX)

accuracySVM = accuracy_score(y_test,pred_svm)
print("SVM - Accuracy:",accuracySVM)

save(vectorizer, classifierSVM, "XSSSVMModel")
vectorizerSVM, classifierSVM = load("XSSSVMModel.pkl")

#print(type(classiferSVM))
inpSVM = [s]
input_transformedSVM = vectorizerSVM.transform(inpSVM)
predictionSVM = classifierSVM.predict(input_transformedSVM.toarray())
print('Input:', inpSVM)
if predictionSVM:
  print("XSS")
else:
  print("Not XSS")
print('The input is', 'XSS' if predictionSVM else 'Not XSS')
print("===============================================================")


print("Perform Sample Tests...")
print("===============================================================")
print("Gradient Boosting")
print("===============================================================")

from sklearn.ensemble import GradientBoostingClassifier
classifierGradBoost = GradientBoostingClassifier()
classifierGradBoost = classifierGradBoost.fit(trainX, y_train)
#Perform classification on samples in X.
pred_grad=classifierGradBoost.predict(testX)

accuracyGB = accuracy_score(y_test,pred_grad)
print("Gred Boost - Accuracy:",accuracyGB)

save(vectorizer, classifierGradBoost, "XSSGradBoostModel")
vectorizerGradBoost, classifierGradBoost = load("XSSGradBoostModel.pkl")

#print(type(classiferSVM))
inpGradBoost = [s]
input_transformedGB = vectorizerGradBoost.transform(inpGradBoost)
predictionGradBoost = classifierGradBoost.predict(input_transformedGB.toarray())
print('Input:', inpGradBoost)
if predictionGradBoost:
  print("XSS")
else:
  print("Not XSS")
print('The input is', 'XSS' if predictionGradBoost else 'Not XSS')
print("===============================================================")


print("Perform Sample Tests...")
print("===============================================================")
print("Logistic Regression")
print("===============================================================")
from sklearn.linear_model import LogisticRegression
classifierLR = LogisticRegression(solver='liblinear',C=10.0, random_state=0)
#Fit the SVM model according to the given training data.
classifierLR = classifierLR.fit(trainX, y_train)
#Perform classification on samples in X.
predLR=classifierLR.predict(testX)

accuracyLR = accuracy_score(y_test,predLR)
print("LR - Accuracy:",accuracyLR)

save(vectorizer, classifierLR, "XSSLRModel")
vectorizerLR, classifierLR = load("XSSLRModel.pkl")

#print(type(classiferSVM))
inpLR = [s]
input_transformedLR = vectorizerLR.transform(inpLR)
predictionLR = classifierLR.predict(input_transformedLR.toarray())
print('Input:', inpLR)
if predictionLR:
  print("XSS")
else:
  print("Not XSS")
print('The input is', 'XSS' if predictionLR else 'Not XSS')
print("===============================================================")
