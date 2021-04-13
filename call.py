import requests, sys


if len(sys.argv) > 1:
    text = sys.argv[1]
else:
    text = "Another test"

url = f"http://localhost:56733/?text={text}"
print(f"This is the response: {requests.get(url).text}")