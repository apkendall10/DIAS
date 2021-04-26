#!/bin/bash

# specify parameters
replica_count=3
num_clients=(1 100)

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
		python3 perf.py -n ${client} -c ${total_clients} -r ${replica_count} &
		#echo "Client: ${client}, total clients: ${total_clients}, replicas: ${replica_count}"
	done

	# synchronously wait
	wait
	echo "Measurement for ${total_clients} clients completed for ${replica_count} replicas!"

done
wait
