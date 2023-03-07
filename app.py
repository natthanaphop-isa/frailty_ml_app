import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd 


#Creating a basic flask app -> the starting point of the application 
app = Flask(__name__)
##load ML 
model = pickle.load(open('logistic_model_frailty.pkl','rb'))


@app.route('/')
def home():
    #create a home html page
    ##it will look at template folder
    return render_template('home.html')

#create an api
@app.route('/predict_api', methods = ['POST'])

def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = np.array(list(data.values())).reshape(1,-1)
    #new_data = pd.json_normalize((data.values()))
    output = model.predict(new_data)
    print(output[0])
    return str(output[0])

@app.route('/predict', methods = ['POST'])
def predict():
    ##create a form to get input from users
    data=[float(x) for x in request.form.values()]
    final_input = np.array(data).reshape(1,-1)
    ##if you have data transformation, you do it here
    output = model.predict(final_input)[0]
    def result():
        if str(output) == "1":
            result = "FRAIL"
        else:
            result = "ROBUST"
        return result
    end = result()
    return render_template("home.html", prediction_text = "Frailty Result: You are {}!".format(end))

if __name__ == "__main__":
    app.run(debug=True)