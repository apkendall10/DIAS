import requests, time

url = f"http://localhost:8001/predict"

text = 'test'
params = {'Input': text, 
          'Category': 'NLP',
          'Task': 'fakenews'}

for epoch in range(10):
    tic = time.time()
    for _ in range(100):
        requests.post(url, json=params)
    elapsed = round(time.time()-tic,3)
    print(f'Epoch {epoch+1}: {elapsed}, {100/elapsed}')