"""
Toy script to ping the worker end-point
Parses command line text and uses it as an arugment in the request
"""

import requests, sys

if len(sys.argv) > 1:
    text = sys.argv[1]
else:
    text = "test"

url = f"http://localhost:8001/predict"
# non-docker test url = 'http://127.0.0.1:5000/'
params = {'Input': text, 
          'Category': 'NLP',
          'Task': 'fakenews'}

r = requests.post(url, json=params)
if r.status_code != 200:
    print(r.text)
else:
    print(f"This is the response: {r.text}")