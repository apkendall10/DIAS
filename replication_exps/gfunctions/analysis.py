import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_size = 129508.092
#data_size = 129
#data_size = 62000
#categories = ["with_autoscale", "without_autoscale"]
categories = ["with_autoscale"]
num_clients = [1, 5, 10, 20, 40, 80, 160]

def average(lst):
    return float(sum(lst)) / len(lst)

def read_file(path):

	content = ""
	with open(path, "r") as file:
		content = file.readlines()

	return content

def make_memory_graph():

	mem_usage = []
	mem_usage_auto_scale = []
	for category in categories:
		clients = [int(x) for x in next(os.walk(category))[1]]

		for client in sorted(clients):
			client = str(client)

			node_mem = []
			path = os.path.join(category, client, "memory")
			for file in os.listdir(path):

				data = [int(x.strip("%\n")) for x in read_file(os.path.join(path, file))]
				node_mem.append(average(data))

			if category == "with_autoscale":
				mem_usage_auto_scale.append(average(node_mem))
			else:
				mem_usage.append(average(node_mem))

	df=pd.DataFrame({'# of clients': num_clients , 'Auto-Scale-max-70': mem_usage_auto_scale, 'Static': mem_usage})
 
	# multiple line plots
	plt.plot( '# of clients', 'Auto-Scale-max-70', data=df, color='red', linewidth=2)
	plt.plot( '# of clients', 'Static', data=df, color='blue', linewidth=2)
	
	plt.legend()
	plt.xlabel("# of clients")
	plt.ylabel("Memory Usage (%)")

	# show graph
	plt.show()

def make_cpu_graph():

	cpu_usage = []
	cpu_usage_auto_scale = []
	for category in categories:
		clients = [int(x) for x in next(os.walk(category))[1]]

		for client in sorted(clients):
			client = str(client)

			node_cpu = []
			path = os.path.join(category, client, "cpu")
			for file in os.listdir(path):

				data = [int(x.strip("%\n")) for x in read_file(os.path.join(path, file))]
				node_cpu.append(average(data))

			if category == "with_autoscale":
				cpu_usage_auto_scale.append(average(node_cpu))
			else:
				cpu_usage.append(average(node_cpu))

	df=pd.DataFrame({'# of clients': num_clients, 'Auto-Scale-cpu': cpu_usage_auto_scale, 'Static-cpu': cpu_usage})
 
	# multiple line plots
	plt.plot( '# of clients', 'Auto-Scale-cpu', data=df, color='red', linewidth=2)
	plt.plot( '# of clients', 'Static-cpu', data=df, color='blue', linewidth=2)

	mem_usage = []
	mem_usage_auto_scale = []
	for category in categories:
			clients = [int(x) for x in next(os.walk(category))[1]]

			for client in sorted(clients):
					client = str(client)

					node_mem = []
					path = os.path.join(category, client, "memory")
					for file in os.listdir(path):

							data = [int(x.strip("%\n")) for x in read_file(os.path.join(path, file))]
							node_mem.append(average(data))

					if category == "with_autoscale":
							mem_usage_auto_scale.append(average(node_mem))
					else:
							mem_usage.append(average(node_mem))

	df=pd.DataFrame({'# of clients': num_clients , 'Auto-Scale-mem': mem_usage_auto_scale, 'Static-mem': mem_usage})

	# multiple line plots
	plt.plot( '# of clients', 'Auto-Scale-mem', data=df, color='red', linewidth=2, linestyle='dashed')
	plt.plot( '# of clients', 'Static-mem', data=df, color='blue', linewidth=2, linestyle='dashed')

	plt.legend()
	plt.xlabel("# of clients")
	plt.ylabel("Usage (%)")

	# show graph
	plt.show()

def make_pods_graph():

	pod_usage = []
	pod_usage_auto_scale = []
	for category in categories:
		clients = [int(x) for x in next(os.walk(category))[1]]

		for client in sorted(clients):
			client = str(client)

			node_pod = []
			path = os.path.join(category, client, "pods")
			for file in os.listdir(path):

				data = [int(x.strip("\n")) for x in read_file(os.path.join(path, file))]
				node_pod.append(average(data))

			if category == "with_autoscale":
				pod_usage_auto_scale.append(average(node_pod))
			else:
				pod_usage.append(average(node_pod))

	df=pd.DataFrame({'# of clients': num_clients , 'Auto-Scale': pod_usage_auto_scale, 'Static': pod_usage})
 
	# multiple line plots
	plt.plot( '# of clients', 'Auto-Scale', data=df, color='red', linewidth=2)
	plt.plot( '# of clients', 'Static', data=df, color='blue', linewidth=2)
	
	plt.legend()
	plt.xlabel("# of clients")
	plt.ylabel("# of active pods")

	# show graph
	plt.show()

def make_throughput_graph():

	throughput = []
	throughput_auto_scale = []
	for category in categories:
		clients = [int(x) for x in next(os.walk(category))[1]]

		for client in sorted(clients):
			client = str(client)
			print(client)

			th = []
			path = os.path.join(category, client)
			for file in os.listdir(path):
				if "total" in file:
					total_latency = float([x.strip("0,\n") for x in read_file(os.path.join(path, file))][1])
					th.append((data_size*int(client))/total_latency)

			if category == "with_autoscale":
				throughput_auto_scale.append(average(th))
			else:
				throughput.append(average(th))

	print(throughput_auto_scale)
	df=pd.DataFrame({'# of clients': num_clients , 'Auto-Scale-max-70': throughput_auto_scale})
	#df=pd.DataFrame({'# of clients': num_clients, 'Static': throughput})
 
	# multiple line plots
	plt.plot( '# of clients', 'Auto-Scale-max-70', data=df, color='red', linewidth=2)
	#plt.plot( '# of clients', 'Static', data=df, color='blue', linewidth=2)
	
	#plt.legend()
	plt.xlabel("# of clients")
	plt.ylabel("Throughput (KB/s)")

	# show graph
	plt.show()

def main():

	# Graph 1
	## y-axis throughput
	## x-axis number of clients
	## For both auto_scale and without_autoscale
	#make_memory_graph()

	# Graph 2
	## y - axis memory
	## x-axis number of clients
	## For both auto_scale and without_autoscale
	#make_cpu_graph()

	# Graph 3
	## y - axis cpu
	## x-axis number of clients
	## For both auto_scale and without_autoscale
	#make_pods_graph()

	# Graph 4
	## y - axis pods
	## x-axis number of clients
	## For both auto_scale and without_autoscale
	make_throughput_graph()

if __name__ == '__main__':
	main()
