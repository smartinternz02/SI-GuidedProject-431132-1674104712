import flask,render_template
import requests
import json
import pickle
API_KEY = "zREBghloyhF7orPL33XUcU6ixLP--pra34YrfZ4NeM73"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

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
  
   #pred = prediction[0]
   
   #print(prediction)
   
   

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": ["average_airflow","average_float","ironfeed","aminaflow","ph","density"], "values": [x]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/01b619ed-9137-4c21-9f75-3a620c0c82fe/predictions?version=2023-02-04', json=payload_scoring,
    headers={'Authorization':'Bearer '+ mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = prediction[0]
    print(prediction)
    print(response_scoring.json())

    return render_template('index.html', prediction_text='Predicted Quality:{}'.format(pred))

if __name__ == "__main__":
    app.run(debug=False)