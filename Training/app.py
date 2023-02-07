from flask import Flask, render_template,request
import numpy as np
import pickle
import pandas as pd

import json

model = pickle.load(open("mining.pkl",'rb'))

app = Flask(__name__)

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "zREBghloyhF7orPL33XUcU6ixLP--pra34YrfZ4NeM73"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/y_predict", methods=['POST'])
def y_predict():
   x_test = [[x for x in request.form.values()]]
   #print(x)
   # NOTE: manually define and pass the array(s) of values to be scored in the next line
   payload_scoring = {"input_data": [{"field": [["avg_air","avg_float","ironfeed","aminaflow","ph","density"]], "values":x_test}]}

   response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/45d58753-6745-46c3-a88f-36f5580cfd98/predictions?version=2022-06-27', json=payload_scoring,
   headers={'Authorization': 'Bearer ' + mltoken})
   predictions=response_scoring.json()
   prediction=model.predict(x_test)
   pred = prediction[0]
   print(prediction)
   
  
   return render_template('index.html', prediction_text='Predicted Quality:{}'.format(pred))

if __name__ == "__main__":
    app.run(debug=False)
