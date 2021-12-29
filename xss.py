import pickle
class xss:

    def __init__(self,url):
        self.url=url
        self.op=0

    def resultSVM(self):
        inp = [self.url]
        with open('XSSSVMModel.pkl', 'rb') as file:
            vectorizerSVM, classifierSVM = pickle.load(file)

        input_transformedSVM = vectorizerSVM.transform(inp)
        predictionSVM = classifierSVM.predict(input_transformedSVM.toarray())
        if predictionSVM:
            #return "XSS"
            #print("SVM - XSS")
            self.op=self.op+1
        else:
            #return "Not XSS"
            #print("SVM - Not XSS")
            self.op=self.op+0

    def resultGB(self):
        inp = [self.url]
        with open('XSSGradBoostModel.pkl', 'rb') as file:
            vectorizerGB, classifierGB = pickle.load(file)

        input_transformedGB = vectorizerGB.transform(inp)
        predictionGB = classifierGB.predict(input_transformedGB.toarray())
        if predictionGB:
            #return "XSS"
            #print("GB - XSS")
            self.op=self.op+1
        else:
            #return "Not XSS"
            #print("GB - Not XSS")
            self.op=self.op+0

    def resultLR(self):
        inp = [self.url]
        with open('XSSLRModel.pkl', 'rb') as file:
            vectorizerLR, classifierLR = pickle.load(file)

        input_transformedLR = vectorizerLR.transform(inp)
        predictionLR = classifierLR.predict(input_transformedLR.toarray())
        if predictionLR:
            #return "XSS"
            #print("LR - XSS")
            self.op=self.op+1
        else:
            #return "Not XSS"
            #print("LR - Not XSS")
            self.op=self.op+0
            
    def result(self):
        if self.op>=2:
            return "XSS"
        else:
            return "Secure"



