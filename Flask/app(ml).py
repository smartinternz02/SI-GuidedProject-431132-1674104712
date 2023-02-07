from flask import Flask, render_template, request
import numpy as np
import pickle
import pandas as pd

model = pickle.load(open('mining.pkl','rb'))

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")      
def about():
    return render_template('about.html')

@app.route("/y_predict", methods=['POST'])
def y_predict():
   x_test = [[x for x in request.form.values()]]
   prediction=model.predict(x_test)
   pred = prediction[0]
   print(prediction)
   
   return render_template('index.html', prediction_text='Predicted Quality:{}'.format(pred))

if __name__ == "__main__":
    app.run(debug=False)

