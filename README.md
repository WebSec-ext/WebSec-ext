
# **WebSec-ext**

https://github.com/WebSec-ext/WebSec-ext


Prerequisites:

1. XAMPP server
2. Python 3

Easy Installation steps :

1. Download and Install Python3

        https://www.python.org/downloads/

2. Download and Install XAMPP

        https://www.apachefriends.org/download.html

3. After the successful installation, open the below mentioned location,
In windows:

        C:\xampp\htdocs\

4. Download the Websec-ext file from github.

        git clone https://github.com/WebSec-ext/WebSec-ext.git

5. open a terminal

6. Train the models and create the machine learning models

        python3 train-codeinj.py
        python3 train-phishing.py
        python3 train-sql.py
        python3 train-xss.py

    After the Successful execution,It will creates machine leraning models

    Creted models are,


            o CodeInjLRModel.pkl
            o CodeInjNaiveModel.pkl
            o CodeInjSVMModel.pkl
            o PhishingDTModel.pkl
            o PhishingLRModel.pkl
            o PhishingRFModel.pkl
            o SQLiDTModel.pkl
            o SQLiLogisticRegModel.pkl
            o SQLiNaiveModel.pkl
            o XSSGradBoostModel.pkl
            o XSSLRModel.pkl
            o XSSSVMModel.pkl
        
7. load the extension to the browser,

        chrome: settings -> Extensions -> Load Unpacked -> Select the Websec-ext directory. 
    
8. Run the extension