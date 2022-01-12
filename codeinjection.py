import pickle
class codeinjection:

    def __init__(self,url):
        self.url=url
        self.op=0

    def resultSVM(self):
        predictionSVM=0
        inp = [self.url]
        with open('CodeInjSVMModel.pkl', 'rb') as file:
            vectorizerSVM, classifierSVM = pickle.load(file)
        input_transformedSVM = vectorizerSVM.transform(inp)
        predictionSVM = classifierSVM.predict(input_transformedSVM.toarray())
        if predictionSVM:
            #return "Code Injection"
            self.op=self.op+1
        else:
            #return "Not Code Injection"
            self.op=self.op+0

    def resultLogisticRegression(self):
        predictionLR=0
        inp = [self.url]
        with open('CodeInjLRModel.pkl', 'rb') as file:
            vectorizerLR, classifierLR = pickle.load(file)
        input_transformedLog = vectorizerLR.transform(inp)
        predictionLR = classifierLR.predict(input_transformedLog.toarray())
        if predictionLR:
            #return "Code Injection"
            self.op=self.op+1
        else:
            #return "Not Code Injection"
            self.op=self.op+0

    def resultGNB(self):
        predictionNB=0
        inp = [self.url]
        with open('CodeInjNaiveModel.pkl', 'rb') as file:
            vectorizerNB, classifierNB = pickle.load(file)
        input_transformedNB = vectorizerNB.transform(inp)
        predictionNB = classifierNB.predict(input_transformedNB.toarray())
        if predictionNB:
            #return "Code Injection"
            self.op=self.op+1
        else:
            #return "Not Code Injection"
            self.op=self.op+0
    

    def result(self):
        if self.op>=2:
            return "Code"
        else:
            return "Secure"

