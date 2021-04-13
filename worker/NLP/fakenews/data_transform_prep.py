"""
Example script to construct the needed pipeline.joblib for the logistic regression model
Note that we dump the pipeline.transform function. This is because we expect pipeline.joblib to contain a collable function
This data_transform_prep script could contain arbitrary complex functions
"""

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import joblib

vect, svd = joblib.load("transformers.joblib")
pipeline = Pipeline(steps=[("tfid", vect), ("svd", svd)])

joblib.dump(pipeline.transform, 'pipeline.joblib')