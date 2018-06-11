import os
import dill as pickle
from sklearn import linear_model, svm, neighbors, gaussian_process, tree, ensemble, neural_network

def get_prefix(data_type):
	if data_type == "model":
		return "models/model_v"
	elif data_type == "data":
		return "models/data_v"
	else:
		exit(1)

def get_version(prefix, delete=False):
	version = 1
	found = False
	while not found:
		filename = prefix + str(version) + ".pk"
		if os.path.exists(filename):
			if delete:
				os.remove(filename)
		else:
			return version

		version += 1

def update(data_type, data):
	prefix = get_prefix(data_type)
	filename = prefix + str(get_version(prefix)) + ".pk"
	with open(filename, "wb") as file:
		pickle.dump(data, file)
	return

def load(data_type, version=-1):
	prefix = get_prefix(data_type)
	if version == -1:
		version = get_version(prefix)-1
	filename = prefix + str(version) + ".pk"
	with open(filename, "rb") as file:
		return pickle.load(file)	

def clean_elem(data_type):
	prefix = get_prefix(data_type)
	v = get_version(prefix, True)	

def clean():
	clean_elem("model")
	clean_elem("data")

