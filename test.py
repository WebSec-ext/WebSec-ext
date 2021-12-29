import sys
from xss import *
from sql import *
from codeinjection import *
from phishing import *
import requests
class test:
    def __init__(self,data):
        self.url=data
        self.output=""

    def callXSS(self):
        objxss=xss(self.url)
        objxss.resultSVM()
        objxss.resultGB()
        objxss.resultLR()
        return objxss.result()

    def callSQL(self):
        objsql=sql(self.url)
        objsql.resultDecisionTree()
        objsql.resultNaiveBayes()
        objsql.resultLogisticRegression()
        return objsql.result()

    def callCodeInj(self):
        objcodeInj=codeinjection(self.url)
        objcodeInj.resultGNB()
        objcodeInj.resultSVM()
        objcodeInj.resultLogisticRegression()
        return objcodeInj.result()

    def callPhishing(self):
        objphishing=phishing(self.url)
        objphishing.resultRandomForest()
        objphishing.resultDecisionTree()
        objphishing.resultLogisticRegression()
        return objphishing.result()
    

def main():
    mainVal=0
    url=str(sys.argv[1])
    urlD = requests.utils.unquote(url)
    objTest = test(urlD)
    if objTest.callXSS()=="XSS":
        mainVal=mainVal+2
    if objTest.callSQL()=="SQLi":
        mainVal=mainVal+1
    if objTest.callCodeInj()=="Code":
        mainVal=mainVal+5
    if objTest.callPhishing()=="Phishing":
        mainVal=mainVal+10
    #print(str(mainVal))
    #print("XSS : "+str(objTest.callXSS())+"SSCode : "+str(objTest.callCodeInj())+"SSSQLi : "+str(objTest.callSQL()))
    #if objTest.output=="":
    #    print("Secure")
    #else:
    #    print("Vulnerable to "+objTest.output+" attacks")
    if mainVal==0:
        print("Secure!")
    elif mainVal==1:
        print("Vulnerable to SQLi")
    elif mainVal==2:
        print("Vulnerable to XSS")
    elif mainVal==3:
        print("Vulnerable to SQLi,XSS")
    elif mainVal==5:
        print("Vulnerable to Code Injection")
    elif mainVal==6:
        print("Vulnerable to SQLi, Code Injection")
    elif mainVal==7:
        print("Vulnerable to XSS, Code Injection")
    elif mainVal==8:
        print("Vulnerable to SQLi, XSS, Code Injection")
    elif mainVal==10:
        print("Vulnerable to Phishing")
    elif mainVal==11:
        print("Vulnerable to SQLi, Phishing")
    elif mainVal==12:
        print("Vulnerable to XSS, Phishing")
    elif mainVal==13:
        print("Vulnerable to SQLi, XSS, Phishing")
    elif mainVal==15:
        print("Vulnerable to Code Injection, Phishing")
    elif mainVal==16:
        print("Vulnerable to SQLi, Code Injection, Phishing")
    elif mainVal==17:
        print("Vulnerable to XSS, Code Injection, Phishing")
    elif mainVal==18:
        print("Vulnerable to SQLi, XSS, Code Injection, Phishing")
    else:
        print("Prediction failed")

if __name__ == "__main__":
    main()