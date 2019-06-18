
#Node Emulation Reservation
from xml.dom import minidom
import os
import sys
import numpy as np
import random
import math
import networkx as nx
import time
import sklearn.cluster as cluster
import json
from subprocess import  call
from flask import jsonify, abort


def reserve_node_emulation(xml_file_path, available_nodes, use_topology_mapping):
	from xml.dom import minidom
	import os
	import sys
	import numpy as np
	import random
	import math
	import networkx as nx
	import time
	import sklearn.cluster as cluster

	U_A = 1
	U_B = 0.8899
	U_C = 0.004197
	CAPACITY_LIMIT = 1000
	INF = 1000000.0
	NODE_CAPACITY = 4389.86
	EPSILON = 0.01

	class TopologyMapping:

		def __init__(self, numOfPhysicalNodes, numOfSimNodes, topology_links, exp_time):
			print(numOfPhysicalNodes, numOfSimNodes, topology_links, exp_time)
			self.N = numOfSimNodes
			self.P = numOfPhysicalNodes
			self.topology_links = topology_links
			self.exp_time = exp_time
			self.total_traffic = 0.0
			self.sim_1_time = 0.0
			self.sim_1_utilization = 0.0
			self.topology = [[0.0 for j in range(self.N)] for i in range(self.N)]
			self.best_mapping = [0, 0, 0, 0, 0, 0, []]

		def build_topology(self):
			for link in self.topology_links:
				self.topology[link[0] - 1][link[1] - 1] = link[2] / 1000000
				self.topology[link[1] - 1][link[0] - 1] = link[2] / 1000000
			for i in range(self.N):
				for j in range(i + 1, self.N):
					self.total_traffic += self.topology[i][j]

		def compute_sim_time(self, traffic):
			time = traffic * 2 * 2 * self.exp_time / NODE_CAPACITY
			return time

		def compute_emu_time(self, traffic):
			time = traffic * self.exp_time / CAPACITY_LIMIT
			return time

		def compute_utilization(self, traffic):
			u = U_A - U_B * math.exp(-U_C * traffic)
			return u

		def evaluate_mapping(self, mapping):
			total_traffic = [[0.0 for j in range(self.P)] for i in range(self.P)]
			min_node = INF
			max_node = 0.0
			max_link = 0.0
			for i in range(self.N):
				for j in range(i + 1, self.N):
					total_traffic[mapping[i]][mapping[j]] += self.topology[i][j]
					if (mapping[i] != mapping[j]):
						total_traffic[mapping[i]][mapping[i]] += self.topology[i][j] / 2
						total_traffic[mapping[j]][mapping[j]] += self.topology[i][j] / 2
						if (total_traffic[mapping[i]][mapping[j]] > max_link):
							max_link = total_traffic[mapping[i]][mapping[j]]
			for i in range(self.P):
				if (total_traffic[i][i] < min_node and total_traffic[i][i] > 0.0):
					min_node = total_traffic[i][i]
				if (total_traffic[i][i] > max_node):
					max_node = total_traffic[i][i]
			sim_time = self.compute_sim_time(max_node)
			emu_time = self.compute_emu_time(max_link)
			utilization = self.compute_utilization(min_node)
			fitness = 0.0
			time_gain = (1 - max(sim_time, emu_time) / self.sim_1_time)
			utilization_loss = (1 - utilization / self.sim_1_utilization)
			if (max_link <= CAPACITY_LIMIT):
				fitness = (self.sim_1_time / (self.sim_1_utilization * 100)) * time_gain - utilization_loss
			return fitness, (1 - max(sim_time, emu_time) / self.sim_1_time) + EPSILON, (
						1 - utilization / self.sim_1_utilization) + EPSILON, min_node, max_node, max_link

		def get_mapping(self, p):
			clustering = cluster.SpectralClustering(n_clusters=p, affinity='precomputed').fit_predict(
				np.array(self.topology))
			return clustering.tolist()

		def get_best_mapping(self):
			self.build_topology()
			self.sim_1_time = self.compute_sim_time(self.total_traffic)
			self.sim_1_utilization = self.compute_utilization(self.total_traffic)
			fitness = 0.0
			for p in range(min(self.N, self.P)):
				start = time.time()
				mapping = self.get_mapping(p + 1)
				fitness, gain, utilization, min_node, max_node, max_link = self.evaluate_mapping(mapping)
				print(mapping, fitness)
				end = time.time()
				if (fitness > self.best_mapping[5]):
					self.best_mapping[0] = min_node
					self.best_mapping[1] = max_node
					self.best_mapping[2] = max_link
					self.best_mapping[3] = gain
					self.best_mapping[4] = utilization
					self.best_mapping[5] = fitness
					self.best_mapping[6] = mapping
			return (self.best_mapping[6])

	if (len(available_nodes) > 0):
		xml_file = minidom.parse(xml_file_path)
		if (use_topology_mapping):
			# Build Topology
			node_index = 1
			topology_links = []
			node_name_list = []
			nodes_mapping = {}

			items = xml_file.getElementsByTagName('networkHardware')

			for NH in items:
				ConnectedNodes = NH.getElementsByTagName('connectedNodes')[0]
				dataRate = NH.getElementsByTagName('dataRate')[0].firstChild.data
				names = ConnectedNodes.getElementsByTagName("name")
				first_node = 0
				second_node = 0
				for name in names:
					node = name.firstChild.data
					if (first_node == 0):
						if (node in node_name_list):
							first_node = nodes_mapping[node] + 1
						else:
							first_node = node_index
							node_name_list.append(node)
							nodes_mapping[node] = node_index - 1
							node_index += 1
					else:
						if (node in node_name_list):
							second_node = nodes_mapping[node] + 1
						else:
							second_node = node_index
							node_name_list.append(node)
							nodes_mapping[node] = node_index - 1
							node_index += 1
						topology_links.append([first_node, second_node, float(dataRate)])

			# Minimum Cut Application
			N = node_index - 1
			exp_time = 30
			topology_mapping = TopologyMapping(len(available_nodes), N, topology_links, exp_time)
			mapping = topology_mapping.get_best_mapping()

			# Update XML File
			num_of_vms = len(set(mapping))

			nodes_config = []
			used_nodes = []
			f = open("/etc/dnsmasq.d/testbed.conf", "r")
			# f=open("/home/nada/CRC/testbed.conf", "r")
			#f = open("/home/debian2/Downloads/testbed.conf", "r")
			lines = f.readlines()
			count = 0
			for line in lines:
				line = line.split(",")
				if (len(line) == 4 and line[2] in available_nodes):
					nodes_config.append([line[2], line[3], line[1]])
					used_nodes.append(line[2])
					count = count + 1
				if (count == num_of_vms):
					break

			to_be_updated_nodes = []
			for link in topology_links:
				if (mapping[link[0] - 1] != mapping[link[1] - 1]):
					if (node_name_list[link[0] - 1] not in to_be_updated_nodes):
						to_be_updated_nodes.append(node_name_list[link[0] - 1])
					if (node_name_list[link[1] - 1] not in to_be_updated_nodes):
						to_be_updated_nodes.append(node_name_list[link[1] - 1])

			NH = xml_file.getElementsByTagName('NetworkHardwares')[0]

			for node in to_be_updated_nodes:
				networkHardware = xml_file.createElement('networkHardware')
				NH.appendChild(networkHardware)

				hidden = xml_file.createElement('hidden')
				hidden.appendChild(xml_file.createTextNode('true'))
				networkHardware.appendChild(hidden)

				t = xml_file.createElement('type')
				t.appendChild(xml_file.createTextNode('Emu'))
				networkHardware.appendChild(t)

				name = xml_file.createElement('name')
				name.appendChild(xml_file.createTextNode('emu_' + node))
				networkHardware.appendChild(name)

				dataRate = xml_file.createElement('dataRate')
				dataRate.appendChild(xml_file.createTextNode('100000000'))
				networkHardware.appendChild(dataRate)

				linkDelay = xml_file.createElement('linkDelay')
				linkDelay.appendChild(xml_file.createTextNode('1000'))
				networkHardware.appendChild(linkDelay)

				enableTrace = xml_file.createElement('enableTrace')
				enableTrace.appendChild(xml_file.createTextNode('true'))
				networkHardware.appendChild(enableTrace)

				tracePromisc = xml_file.createElement('tracePromisc')
				tracePromisc.appendChild(xml_file.createTextNode('true'))
				networkHardware.appendChild(tracePromisc)

				iface = xml_file.createElement('iface')
				iface.appendChild(xml_file.createTextNode('eth0'))
				networkHardware.appendChild(iface)

				connectedNodes = xml_file.createElement('connectedNodes')
				networkHardware.appendChild(connectedNodes)
				n = xml_file.createElement('name')
				n.appendChild(xml_file.createTextNode(node))
				connectedNodes.appendChild(n)

			gen = xml_file.getElementsByTagName('Gen')[0]
			NHs = xml_file.getElementsByTagName('networkHardware')
			all_nodes = xml_file.getElementsByTagName('node')

			for node in all_nodes:
				name = node.getElementsByTagName('name')[0].firstChild.data
				if (name in to_be_updated_nodes):
					# parent = node.parentNode
					# parent.removeChild(node)
					pass
				else:
					VM = node.getElementsByTagName('VM')[0]
					parent = VM.parentNode
					parent.removeChild(VM)

			nodes = xml_file.getElementsByTagName("VMs")
			for node in nodes:
				parent = node.parentNode
				parent.removeChild(node)

			nodes = xml_file.getElementsByTagName("usedVMs")
			for node in nodes:
				parent = node.parentNode
				parent.removeChild(node)

			VMs = xml_file.createElement('VMs')
			gen.appendChild(VMs)

			for node in nodes_config:
				VM = xml_file.createElement('VM')
				VMs.appendChild(VM)

				realName = xml_file.createElement('realName')
				realName.appendChild(xml_file.createTextNode(node[0]))
				VM.appendChild(realName)

				name = xml_file.createElement('name')
				name.appendChild(xml_file.createTextNode(node[0]))
				VM.appendChild(name)

				IP = xml_file.createElement('IP')
				IP.appendChild(xml_file.createTextNode(node[1].replace('\n', '')))
				VM.appendChild(IP)

				MAC = xml_file.createElement('MAC')
				MAC.appendChild(xml_file.createTextNode(node[2]))
				VM.appendChild(MAC)

			for child in NHs:
				usedVMs = xml_file.createElement('usedVMs')
				child.appendChild(usedVMs)

				ConnectedNodes = child.getElementsByTagName('connectedNodes')[0]
				names = ConnectedNodes.getElementsByTagName("name")

				for name in names:
					text = name.firstChild.data
					VM = xml_file.createElement('name')
					VM.appendChild(xml_file.createTextNode(used_nodes[mapping[nodes_mapping[text]]]))
					usedVMs.appendChild(VM)

			for node in all_nodes:
				name = node.getElementsByTagName("name")[0].firstChild.data
				VM = xml_file.createElement('VM')
				VM.appendChild(xml_file.createTextNode(used_nodes[mapping[nodes_mapping[name]]]))
				node.appendChild(VM)

			apps = xml_file.getElementsByTagName('application')
			for app in apps:
				senderNode = app.getElementsByTagName("sender")[0].firstChild.data
				recieverNode = app.getElementsByTagName("receiver")[0].firstChild.data

			app.getElementsByTagName("senderVM")[0].firstChild.data = used_nodes[mapping[nodes_mapping[senderNode]]]
			app.getElementsByTagName("receiverVM")[0].firstChild.data = used_nodes[mapping[nodes_mapping[recieverNode]]]

			new_XML = open(xml_file_path, "w")
			gen = gen.toprettyxml(indent='\t')
			text = "".join([s for s in gen.strip().splitlines(True) if s.strip()])
			new_XML.write(text)
			new_XML.close()

			return used_nodes

		else:
			VMs = xml_file.getElementsByTagName('VM')
			used_nodes = []
			available = True
			for VM in VMs:
				realName = VM.getElementsByTagName('realName')[0].firstChild.data
				used_nodes.append(realName)
				if (realName not in available_nodes):
					available = False
					break
			if (available):
				return used_nodes
			else:
				return []
	else:
		return []


# ------------------------------------------------------------------------------------------------------------------------------------

# Node Emulation Running

# xml_file_path: string
# task_id: string
def run_node_emulation(xml_file_path, task_id):
	emulation_log_path = '/home/emulation_log/log'
	call(["rm", "-rf", emulation_log_path+"{0}-load.progress".format(task_id)])

	call(["/home/generate_run_scripts", "{0}".format(xml_file_path), ">>", emulation_log_path+"{0}-load.progress".format(task_id)])

# ------------------------------------------------------------------------------------------------------------------------------------

# Node Emulation Status

# task_id: string
def node_emulation_status(task_id):
	emulation_log_path = '/home/emulation_log/log'
	progress_log = emulation_log_path + "{0}-load.progress".format(task_id)
	error = False
	done = False
	progress = "..."

	if os.path.exists(progress_log) == False:
		return abort(400)
	if os.stat(progress_log).st_size > 0:
		with open(progress_log, 'r') as plog:
			std_error = False
			for line in plog:
				if ("OmfCommon: Disconnecting..." in line):
					done = True
					error = std_error
					progress = "Done"
				if ("STDERR" in line):
					std_error = True

	return jsonify({
		'task_id': task_id,
		'progress': progress,
		'error': error,
		'done': done
	})