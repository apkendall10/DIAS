"""
Toy script to ping the worker end-point
Parses command line text and uses it as an arugment in the request
"""

import requests, sys

if len(sys.argv) > 1:
    text = sys.argv[1]
else:
    text = "Another"

url = f"http://localhost:56733/"
# non-docker test url = 'http://127.0.0.1:5000/'
params = {'text': text, 
          'tag': 'fakenews',
          'cat': 'NLP',
          'model_num': '2'}

r = requests.get(url, params = params)
print(r.url)
print(f"This is the response: {r.text}")