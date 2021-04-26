export PROJECT_ID=stately-vector-311213
gcloud config set project stately-vector-311213
cd manager & docker build -t gcr.io/${PROJECT_ID}/manager:latest .
cd ../worker & docker ^Cild -t gcr.io/${PROJECT_ID}/worker:latest .
cd ..
# upload to container registery so GKE can download them
gcloud services enable containerregistry.googleapis.com
# if project unset -> gcloud config set project stately-vector-311213
gcloud auth configure-docker
docker push gcr.io/${PROJECT_ID}/manager:latest
docker push gcr.io/${PROJECT_ID}/worker:latest

# If GKE cluster not setup -> https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app#creating_a_cluster
# if you already have a GKE cluster running -> gcloud container clusters get-credentials my-first-cluster-1 --zone us-central1-c --project stately-vector-311213
kubectl get nodes

# if no deployment conf file -> https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app#deploying_the_sample_app_to

kubectl apply -f k8s/manager.yaml
kubectl apply -f k8s/worker.yaml

kubectl get pods
kubectl get service

# Get the EXTERNAL-IP from above for test.
curl EXTERNAL-IP
python3 call.py


# for logs
kubectl logs svc/dias-manager-svc
kubectl logs svc/dias-worker-svc

# Auto scale
kubectl autoscale deployment dias-worker --cpu-percent=70 --min=1 --max=10
# Check autoscale status
kubectl get hpa
## Scaling based on custom and multiple metrics (like requests per second) can be done 
## https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#autoscaling-on-multiple-metrics-and-custom-metrics



# delete services
kubectl delete service dias-manager-svc dias-worker-svc
# delete images
gcloud container images delete gcr.io/${PROJECT_ID}/manager:latest  --force-delete-tags --quiet
gcloud container images delete gcr.io/${PROJECT_ID}/worker:latest  --force-delete-tags --quiet
# Delete cluster




# https://kubernetes.io/docs/reference/kubectl/cheatsheet/



##############################################
Testing google functions

# Manager
gcloud functions call func-manager --data '{"Input": "test", "Category": "NLP", "Task": "fakenews"}'
# Worker
# gcloud functions call function-test --data '{"Input": "test", "Category": "NLP", "Tag": "fakenews", "Model": 1}'
# Passed as params not json.


