import requests, time
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-n', dest='node', type=int,
                    help='Process number to track output.', default=0)
parser.add_argument('-c', dest='num_clients', type=int,
                    help='Process number to track output.', default=1)

url = f"http://35.202.228.150/predict"

def make_request(text):
    params = {'Input': text, 
          'Category': 'NLP',
          'Task': 'fakenews'}
    requests.post(url, json=params)

def main(node, num_clients):
    latencies = []
    df = pd.read_csv('../all.csv')
    start = time.time()

    for i in range(len(df)):
        row = df.iloc[i]
        tic = time.time()
        make_request(row.text)
        latencies.append(round(time.time() - tic,4))

    total = round(time.time() - start,4)
    pd.Series(latencies).to_csv(f'{num_clients}/latencies_{node}.csv')
    pd.Series([total]).to_csv(f'{num_clients}/total_{node}.csv')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.node, args.num_clients)
