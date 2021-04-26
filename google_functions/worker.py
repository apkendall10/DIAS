from google.cloud import storage
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

def worker_infer(request):
    #request_json = request.get_json()
    try:
        # text = request_json['Input']
        # cat = request_json['Category']
        # tag = request_json['Tag']
        # model_num = request_json['Model']
        text = request.args.get('Input')
        cat = request.args.get('Category')
        tag = request.args.get('Tag')
        model_num = request.args.get('Model')
    except Exception as e:
        # msg = f"Error: incorrect params passed. Expected (text, cat, tag, model_num), recieved {request_json}"
        msg = f"Error: incorrect params passed. Expected (text, cat, tag, model_num), recieved {request.args}"
        logger.error(e)
        logger.error(msg)
        return msg, 400

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
        rel_path = os.path.join(cat, tag, f'model{model_num}')
        try:
            # Need to write tmp files in /tmp because everything else is read only.
            client = storage.Client()
            bucket = client.get_bucket('dias-model-bucket')
            remote_model = bucket.get_blob(os.path.join(rel_path, 'model.joblib'))
            remote_model.download_to_filename('/tmp/local_m.joblib')
            remote_pipeline = bucket.get_blob(os.path.join(rel_path, 'pipeline.joblib'))
            remote_pipeline.download_to_filename('/tmp/local_p.joblib')
            model = joblib.load('/tmp/local_m.joblib')
            pipeline = joblib.load('/tmp/local_p.joblib')
            #model, pipeline = get_details_bucket(cat, tag, model_num)
        except Exception as e:
            msg = f"Error: unable to identify a model with cat = {cat}, tag = {tag}, model_num = {model_num}. Path: {rel_path} Error: {e}"
            logger.error(e)
            logger.error(msg)
            return msg, 400

        sub_tree[model_num] = (model, pipeline)
    
    try:
        data = pipeline([text])
        prediction = model.predict(data)[0]
    except Exception as e:
        msg = f"Error: unable to perform data tranformation and prediction for cat = {cat}, tag = {tag}, model_num = {model_num}"
        logger.error(e)
        logger.error(msg)
        return msg, 400
    #predict_proba returns a single element list of tuples with (prob_true, prob_false)
    #we just display the prob_false - i.e. we answer is this fake?
    return str(prediction), 200
