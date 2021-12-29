import pandas as pd
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB,GaussianNB,ComplementNB,BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
#reading the dataset...
url='https://raw.githubusercontent.com/WebSec-ext/DataSet/main/datasetCD.csv'
df=pd.read_csv(url,error_bad_lines=False,encoding='utf-8')

df = df.dropna(how='any',axis=0)
vectorizer = CountVectorizer( min_df=2, max_df=0.6, max_features=2809, stop_words=stopwords.words('english'))
#Learn the vocabulary dictionary and return document-term matrix.
posts = vectorizer.fit_transform(df['Sentence'].values.astype('U')).toarray()
posts.shape=(5172,53,53,1)
X=posts
Y=df['Label']
#Train Test split...
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


print("Perform Sample Tests...")
print("===============================================================")
print("SVM")
print("===============================================================")

from sklearn.svm import SVC
from sklearn import metrics
classifierSVM = SVC(gamma='auto',kernel='linear')
#Fit the SVM model according to the given training data.
classifierSVM.fit(trainX, Y_train)
#Perform classification on samples in X.
pred_svm=classifierSVM.predict(testX)
'''accuracySVM = accuracy_score(Y_test,pred_svm)
print("Accuracy:",accuracySVM)
from sklearn import metrics'''

print("SVM - Accuracy:",metrics.accuracy_score(Y_test,pred_svm))

save(vectorizer, classifierSVM,"CodeInjSVMModel")
vectorizern, classiferSVMsaved = load("CodeInjSVMModel.pkl")

print('\nPerform a test')                    
#inp = ["An intent filter is an expression in an app's manifest file that specifies the type of intents that the component would like to receive."]
inp = ["\necho INJECTX\nexit\n\033[2Asleep 5\n"]
input_transformed = vectorizern.transform(inp)
predictionSVM = classiferSVMsaved.predict(input_transformed.toarray())
print('Input:', inp)
if predictionSVM:
  print("Code Injection")
else:
  print("Not Code Injection")
print('The input is', 'Code Injection' if predictionSVM else 'Not Code Injection')


print("Perform Sample Tests...")
print("===============================================================")
print("Naive bayes")
print("===============================================================")

gnb = GaussianNB()
classifierGNB = gnb.fit(trainX, Y_train)
#Perform classification on an array of test vectors X.
predGNB = gnb.predict(testX)
accuracyGNB = accuracy_score(Y_test,predGNB)
print("GNB - Accuracy:",accuracyGNB)
save(vectorizer, classifierGNB,"CodeInjNaiveModel")
vectorizer, classiferNaivesaved = load("CodeInjNaiveModel.pkl")

print('\nPerform a test')                    
#inp = ["An intent filter is an expression in an app's manifest file that specifies the type of intents that the component would like to receive."]
inp = ["; net localgroup Administrators hacker /ADD"]
input_transformed = vectorizern.transform(inp)
predictionGNB = classiferNaivesaved.predict(input_transformed.toarray())
print('Input:', inp)
if predictionGNB:
  print("Code Injection")
else:
  print("Not Code Injection")
print('The input is', 'Code Injection' if predictionGNB else 'Not Code Injection')

print("Perform Sample Tests...")
print("===============================================================")
print("Logistic Regression")
print("===============================================================")

classifierLR = LogisticRegression(solver='liblinear',C=10.0, random_state=0)
classifierLR.fit(trainX,Y_train)
pred_LR=classifierLR.predict(testX)
print("Accuracy:",accuracy_score(Y_test, pred_LR))
save(vectorizer, classifierLR,"CodeInjLRModel")
vectorizern, classiferLRsaved = load("CodeInjLRModel.pkl")

print('\nPerform a test')                    
#inp = ["An intent filter is an expression in an app's manifest file that specifies the type of intents that the component would like to receive."]
inp = ["&& netsh firewall set opmode disable"]
input_transformed = vectorizern.transform(inp)
predictionLR = classiferLRsaved.predict(input_transformed.toarray())
print('Input:', inp)
if predictionLR:
  print("Code Injection")
else:
  print("Not Code Injection")
print('The input is', 'Code Injection' if predictionLR else 'Not Code Injection')


