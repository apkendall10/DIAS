import flask
from flask import request, jsonify
import pandas as pd
import numpy as np
import joblib, time
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

#build the data transformation and model
vect, svd = joblib.load("transformers.joblib")
pipeline = Pipeline(steps=[("tfid", vect), ("svd", svd)])
log_reg = joblib.load("logistic_reg.joblib")

#initialize the app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#simple endpoint for now
@app.route('/', methods=['GET'])
def home():
    if 'text' in request.args:
        text = request.args['text']
    else:
        return "Error: no text found"
    print(f'This is the input: {text}')
    data = pipeline.transform([text])
    #predict_proba returns a single element list of tuples with (prob_true, prob_false)
    #we just display the prob_false - i.e. we answer is this fake?
    return str(log_reg.predict_proba(data)[0][1])