import requests, time, joblib
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-n', dest='node', type=int,
                    help='Process number to track output.', default=0)
parser.add_argument('--c', dest='container', action = 'store_true',
                    help='Process number to track output.',)

url = f"http://localhost:8002/predict"

model = joblib.load('worker/NLP/fakenews/model1/model.joblib')
transform = joblib.load('worker/NLP/fakenews/model1/pipeline.joblib')

def local_predict(text):
    model.predict(transform([text]))

def make_request(text):
    params = {'Input': text, 
          'Category': 'NLP',
          'Task': 'fakenews'}
          #'Model': '1'}
    requests.post(url, json=params)

def main(args):
    node = args.node
    container = args.container
    latencies = []
    df = pd.read_csv('all.csv')
    start = time.time()
    for i in range(len(df)):
        row = df.iloc[i]
        tic = time.time()
        if container:
            make_request(row.text)
        else:
            local_predict(row.text)
        latencies.append(round(time.time() - tic,4))
        if i % 250 == 0:
            print(f'{i}, {round(time.time() - start, 4)}')
    total = round(time.time() - start,4)
    pd.Series(latencies).to_csv(f'latencies_{node}.csv')
    pd.Series([total, len(df)]).to_csv(f'total_{node}.csv')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)