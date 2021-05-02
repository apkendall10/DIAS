import requests, time
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-n', dest='node', type=int,
                    help='Process number to track output.', default=0)
parser.add_argument('-c', dest='num_clients', type=int,
                    help='Process number to track output.', default=1)

url = f"http://us-central1-stately-vector-311213.cloudfunctions.net/func-manager"

def make_request(text):
    params = {'Input': text, 
          'Category': 'NLP',
          'Task': 'fakenews'}
    requests.post(url, json=params)

def main(node, num_clients):
    latencies = []
    df = pd.read_csv('../all.csv')
    print(len(df))
    start = time.time()

    for i in range(int(len(df)/2)):
        row = df.iloc[i]
        tic = time.time()
        make_request(row.text[:int(len(row.text)/2)])
        latencies.append(round(time.time() - tic,4))
        tic = time.time()
        make_request(row.text[int(len(row.text)/2):])
        latencies.append(round(time.time() - tic,4))

    total = round(time.time() - start,4)
    pd.Series(latencies).to_csv(f'{num_clients}/latencies_{node}.csv')
    pd.Series([total]).to_csv(f'{num_clients}/total_{node}.csv')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.node, args.num_clients)

