# DIAS
Distributed inference as a service: a course project for CS 739 at UW-Madison

see `steps.sh`

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
