#!/bin/bash
# Functions autoscaled to 35
# Each function instance has 1 GiB memory.

# specify parameters
num_clients=(1 5 10 20 40 80 160)

for total_clients in "${num_clients[@]}"; do
    	# determine if result already computed
	if [ -d "${total_clients}" ]; then
		echo "Result ${total_clients} already exists!"
		continue
	fi

    mkdir -p "${total_clients}"

    echo "Initializing total clients: ${total_clients} ..."

	# do measurement
	for client in $(seq "$total_clients"); do
		python3 performance_test.py -n ${client} -c ${total_clients} &
		# echo "Client: ${client}, total clients: ${total_clients}"
	done

    wait
	echo "Clients: ${total_clients} processed!"
done