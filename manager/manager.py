from requests_futures.sessions import FuturesSession
from flask import Flask, request
import logging
import flask

# Initialize flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True
logger = logging.getLogger()

# System map to determine model addresses
model_lookup_map = {
	"NLP": {"fakenews": {"url": "http://worker/", "models": [1,2,3,4,5], "Info": "Input: Text, Output: Real or Fake News"}},
	"IMAGE": {"catORdog": {"url": "http://worker/", "models": [1,2,3], "Info": "Input: Image, Output: Image of Cat or Dog"}},
}

@app.route('/', methods=['GET'])
def home():
	return "Welcome to DIAS: Distributed Inference as a Service!\n", 200 

@app.route('/predict', methods=['POST'])
def predict():
	
	# Parse input
	try:
		request_data = request.get_json()
		input_ = request_data['Input']
		category_ = request_data['Category']
		task_ = request_data['Task']
	except Exception as e:
		msg = f"Error: incorrect params! Expected (Input, Category, Task), recieved ({', '.join(list(request.args.keys()))})"
		logger.error(e)
		logger.error(msg)
		return msg, 400

	# Get required model details
	try:
		category_URL = model_lookup_map[category_][task_]["url"]
		category_models = model_lookup_map[category_][task_]["models"]
	except Exception as e:
		msg = f"Error: category {category_} and task {task_} is not supported."
		logger.error(e)
		logger.error(msg)
		return msg, 400

	# Send async query to each model
	callbacks = []
	session = FuturesSession()
	for model_num in category_models:
		params = {
			'Input': input_,
			'Category': category_,
			'Tag': task_,
			'Model': model_num,
		}

		future = session.get(category_URL, params=params)
		callbacks.append(future)

	# Wait on the results
	majority_result = []
	for cb in callbacks:
		response = cb.result()
		if response.status_code != 200:
			logger.error(response.text)
			continue
		majority_result.append(response.text)

	# If no worker was able to respond
	if len(majority_result) == 0:
		logger.error("Request to every model failed!")
		return "Error: service has encountered a problem, please contact customer support", 500

	# Send back majority result
	return str(max(set(majority_result), key=majority_result.count)), 200

@app.route('/help', methods=['GET'])
def help():

	return_str = "DIAS currently supports the following categories and tasks:\n\n<Category: Task>\n"
	for category in model_lookup_map:
		for task in model_lookup_map[category]:
			return_str += f"- {category}: {task} ({model_lookup_map[category][task]['Info']})\n"

	return return_str, 200
