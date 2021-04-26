#!/bin/bash

# specify parameters
cpu_thresholds=(15 30 45 60 75 90)
num_clients=(1 100 10000)

# setup environment
gcloud config set project stately-vector-311213
gcloud container clusters get-credentials my-first-cluster-1 --zone us-central1-c --project stately-vector-311213

for replica_count in "${cpu_thresholds[@]}"; do

	# scale number of replicas
	kubectl autoscale deployment dias-worker --cpu-percent=${replica_count} --min=1 --max=35
	kubectl autoscale deployment dias-manager --cpu-percent=${replica_count} --min=1 --max=35
	sleep 2m

	for total_clients in "${num_clients[@]}"; do

		# determine if result already computed
		if [ -d "${total_clients}/${replica_count}" ]; then
			echo "Result ${total_clients}/${replica_count} already exists."
			continue
		fi

		# create directory
		mkdir -p "${total_clients}/${replica_count}"

		# do measurement
		for client in $(seq "$total_clients"); do
			python3 performance_test.py -n ${client} -c ${total_clients} -r ${replica_count} &
			# echo "Client: ${client}, total clients: ${total_clients}, replicas: ${replica_count}"
		done

		# synchronously wait
		wait
		echo " --- Client count: ${total_clients} processed"
	done

	echo "Replica count: ${replica_count} done!"
done
wait
