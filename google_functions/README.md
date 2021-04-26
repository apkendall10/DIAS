To test the functions:  
`gcloud functions call func-manager --data '{"Input": "test", "Category": "NLP", "Task": "fakenews"}'`

Or,
```bash
curl -i --header "Content-Type: application/json" \
	--request POST \
	--data '{"Input": "test", "Category": "NLP", "Task": "fakenews"}' \
	http://us-central1-stately-vector-311213.cloudfunctions.net/func-manager
```


---
- Models stored in `dias-model-bucket`
- Both the functions are set to auto scale upto 10 instances.
- Timeout is set to 60 seconds, after which the instance is killed.
- 1 GiB memory allocated per function instance.
- Models copied from bucket are stored on tmpfs.

