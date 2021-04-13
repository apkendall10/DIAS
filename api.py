import flask
from flask import request, jsonify
import pandas as pd
import numpy as np
import joblib, time
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

vect, svd = joblib.load("transformers.joblib")
pipeline = Pipeline(steps=[("tfid", vect), ("svd", svd)])
log_reg = joblib.load("logistic_reg.joblib")

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    if 'text' in request.args:
        text = request.args['text']
    else:
        return "Error: no text found"
    print(f'This is the input: {text}')
    data = pipeline.transform([text])
    return str(log_reg.predict_proba(data)[0][1])

#app.run()