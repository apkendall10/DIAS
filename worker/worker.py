import flask
from flask import request, jsonify
import numpy as np
import joblib, time, os
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import logging

#initialize bookkeeping data
tree = dict()
logger = logging.getLogger()

#initialize the app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#simple endpoint for now
@app.route('/', methods=['GET'])
def home():
    try:
        text = request.args['text']
        cat = request.args['cat']
        tag = request.args['tag']
        model_num = request.args['model_num']
    except Exception as e:
        msg = f"Error: incorrect params passed. Expected (text, cat, tag, model_num), recieved ({', '.join(list(request.args.keys()))})"
        logger.error(e)
        logger.error(msg)
        return msg

    # Travel through our tree of dictionaries to get to the correct subtree
    # Generate any missing pieces
    sub_tree = tree
    for key in [cat, tag]:
        if not key in sub_tree:
            sub_tree[key] = dict()
        sub_tree = sub_tree[key]
    
    # Check if we already have the details we need to serve
    if model_num in sub_tree:
        model, pipeline = sub_tree[model_num]
    else:
        try:
            model, pipeline = get_details(cat, tag, model_num)
        except Exception as e:
            msg = f"Error: unable to identify a model with cat = {cat}, tag = {tag}, model_num = {model_num}"
            logger.error(e)
            logger.error(msg)
            return msg

        sub_tree[model_num] = (model, pipeline)
    
    data = pipeline([text])
    #predict_proba returns a single element list of tuples with (prob_true, prob_false)
    #we just display the prob_false - i.e. we answer is this fake?
    return str(model.predict_proba(data)[0][1])


def get_details(cat, tag, model_num):
    rel_path = os.path.join(cat, tag, f'model{model_num}')
    model = joblib.load(os.path.join(rel_path, 'model.joblib'))
    pipeline = joblib.load(os.path.join(rel_path, 'pipeline.joblib'))
    return model, pipeline

