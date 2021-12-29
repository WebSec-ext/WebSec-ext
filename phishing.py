import pickle
import featureExtractionPhish
import numpy as np
class phishing:

    def __init__(self,url):
        self.url=url
        self.op=0

    def resultRandomForest(self):
        with open('PhishingRFModel.pkl', 'rb') as file:
            classifierRF = pickle.load(file)
        inp = self.url
        X_new = featureExtractionPhish.generate_data_set(inp)
        X_new = np.array(X_new).reshape(1,-1)
        predictionRF = classifierRF.predict(X_new)
        if predictionRF == -1:
            #return "Phishing"
            self.op=self.op+1
        else:
            #return "Not Phishing"
            self.op=self.op+0

    def resultDecisionTree(self):
        with open('PhishingDTModel.pkl', 'rb') as file:
            classifierDT = pickle.load(file)
        inp = self.url
        X_new = featureExtractionPhish.generate_data_set(inp)
        X_new = np.array(X_new).reshape(1,-1)
        predictionDT = classifierDT.predict(X_new)
        if predictionDT == -1:
            #return "Phishing"
            self.op=self.op+1
        else:
            #return "Not Phishing"
            self.op=self.op+0

    def resultLogisticRegression(self):
        with open('PhishingLRModel.pkl', 'rb') as file:
            classifierLR = pickle.load(file)
        inp = self.url
        X_new = featureExtractionPhish.generate_data_set(inp)
        X_new = np.array(X_new).reshape(1,-1)
        predictionLR = classifierLR.predict(X_new)
        if predictionLR == -1:
            #return "Phishing"
            self.op=self.op+1
        else:
            #return "Not Phishing"
            self.op=self.op+0
    

    def result(self):
        if self.op>1:
            return "Phishing"
        else:
            return "Secure"

