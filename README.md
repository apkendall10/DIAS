TODO:
The worker service `dias-worker-svc` is reachable from manager service `dias-manager-svc`, but /predict fails with
a connection establishment error. This is likely due to an error I see in worker uWSGI logs:\\
`# kubectl logs svc/dias-worker-svc`\\
```
spawned uWSGI worker 1 (pid: 17, cores: 1)
spawned uWSGI worker 2 (pid: 18, cores: 1)
ModuleNotFoundError: No module named 'manager'
unable to load app 0 (mountpoint='') (callable not found or import error)
*** no app loaded. going in full dynamic mode ***
```

Manager service is reachable from external host (GET works).


# DIAS
Distributed inference as a service: a course project for CS 739 at UW-Madison

# Quick Start
Run the start.sh script to start the docker containers for worker and manager:
  ```bash
  sudo bash start.sh
  ```

Check if the service is running at:
  ```bash
  curl http://localhost:8001/
  ```

# Usage
We currently support the following two APIs:

* `/predict`

    Accepts a POST request with the following json fields:
    ```
    json = {'Input': <Input text to ML models>, 
            'Category': <Category of models that need be queried>,
            'Task': <Model type for that category>}
    ```

* `/help`

    Use this route to see the currently supported categories and tasks.

# Example
For Fake News Detection, run the call.py script with the text you want to pass to the system:
  `python call.py 'This is a test of the model'`
