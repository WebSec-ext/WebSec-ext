import pickle
class sql:

    def __init__(self,url):
        self.url=url
        self.op=0

    def resultLogisticRegression(self):
        inp = [self.url]
        with open('SQLiLogisticRegModel.pkl', 'rb') as file:
            vectorizerLogReg, classifierLogReg = pickle.load(file)
        input_transformedLog = vectorizerLogReg.transform(inp)
        predictionLog = classifierLogReg.predict(input_transformedLog.toarray())
        if predictionLog:
            #return "SQLi"
            self.op=self.op+1
        else:
            #return "Not SQLi"
            self.op=self.op+0

    def resultDecisionTree(self):
        inp = [self.url]
        with open('SQLiDTModel.pkl', 'rb') as file:
            vectorizerDT, classifierDT = pickle.load(file)
        input_transformedDT = vectorizerDT.transform(inp)
        predictionDT = classifierDT.predict(input_transformedDT.toarray())
        if predictionDT:
            #return "SQLi"
            self.op=self.op+1
        else:
            #return "Not SQLi"
            self.op=self.op+0

    def resultNaiveBayes(self):
        inp = [self.url]
        with open('SQLiNaiveModel.pkl', 'rb') as file:
            vectorizerNB, classifierNB = pickle.load(file)
        input_transformedNB = vectorizerNB.transform(inp)
        predictionNB = classifierNB.predict(input_transformedNB.toarray())
        if predictionNB:
            #return "SQLi"
            self.op=self.op+1
        else:
            #return "Not SQLi"
            self.op=self.op+0
    

    def result(self):
        if self.op>1:
            return "SQLi"
        else:
            return "Secure"

