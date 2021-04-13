import requests, time

text = 'test'
url = f"http://localhost:56733/?text={text}"

for epoch in range(10):
    tic = time.time()
    for _ in range(100):
        requests.get(url).text
    elapsed = round(time.time()-tic,3)
    print(f'Epoch {epoch+1}: {elapsed}, {100/elapsed}')