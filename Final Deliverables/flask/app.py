import pandas as pd
import numpy as np
import pickle
import os
from flask import Flask,request, render_template

app=Flask(__name__,template_folder="templates")

seconds_in_a_day = 24 * 60 * 60
seconds_in_a_day

app=Flask(__name__,template_folder="templates")
@app.route('/', methods=['GET'])
def index():
    return render_template('\Python Scripts\tamlates\upload.html')
@app.route('/home', methods=['GET'])
def about():
    return render_template('\Python Scripts\home.html')
@app.route('/pred',methods=['GET'])
def page():
    return render_template('\Python Scripts\tamlates\upload.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print("[INFO] loading model...")
    model = pickle.load(open('\Python Scripts\tamlates\foodDemand.pkl', 'rb'))
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    print(features_value)
    
    features_name = ['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine',
       'city_code', 'region_code', 'category']
    prediction = model.predict(features_value)
    output=prediction[0]    
    print(output)
    return render_template('\Python Scripts\tamlates\upload.html', prediction_text=output)

if __name__ == '__main__':
      app.run(debug=False)