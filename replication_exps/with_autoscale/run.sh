#!/bin/bash

# specify parameters
num_clients=(1 5 10 20 40 80 160)

# setup environment
gcloud config set project stately-vector-311213
gcloud container clusters get-credentials dias-cluster --zone us-central1-c --project stately-vector-311213

# delete autoscale
# kubectl delete hpa dias-worker
# kubectl delete hpa dias-manager
# sleep 30s

# autoscale number of replicas
kubectl autoscale deployment dias-worker --cpu-percent=70 --min=1 --max=35
kubectl autoscale deployment dias-manager --cpu-percent=70 --min=1 --max=35
sleep 30s

for total_clients in "${num_clients[@]}"; do

	# determine if result already computed
	if [ -d "${total_clients}" ]; then
		echo "Result ${total_clients} already exists!"
		continue
	fi

	# create directories
	mkdir -p "${total_clients}/cpu"
	mkdir -p "${total_clients}/memory"
	mkdir -p "${total_clients}/pods"

	echo "Initializing total clients: ${total_clients} ..."

	# do measurement
	for client in $(seq "$total_clients"); do
		python3 performance_test.py -n ${client} -c ${total_clients} &
		# echo "Client: ${client}, total clients: ${total_clients}"
	done

	# fetch metrics periodically
	for iter in {1..3}; do
		sleep 2m

		# get total number of pods
		kubectl get po | tail -n+2 | wc -l >> "${total_clients}/pods/${iter}.txt"

		# get cpu usage
		kubectl top nodes | tail -n+2 | awk '{ print $3 }' >> "${total_clients}/cpu/${iter}.txt"

		# get memory usage
		kubectl top nodes | tail -n+2 | awk '{ print $5 }' >> "${total_clients}/memory/${iter}.txt"

	done

	echo "Clients: ${total_clients} metrics saved!"

	# synchronously wait
	wait
	echo "Clients: ${total_clients} processed!"

	# reset the total number of pods
	kubectl scale --replicas=3 deployment/dias-worker
	kubectl scale --replicas=3 deployment/dias-manager
	sleep 30s

done
