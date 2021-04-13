# Worker Setup
Workers use the following file structure cat/tag/model{model_num}
In the root path, there should be two files - model.joblib and pipeline.joblib
- model.joblib should be a created by using joblib.dump with the model object. We expect the model object to have the predict_proba function that accepts a list of strings
- pipeline.joblib should contain a callable function that represents all data transformations required to format a string literal into the format needed for the model to perform inference. We expect the object to have be callable directly