from random import shuffle
import math
import numpy as np

customers = []

def split_data(data):
	shuffle(data)
	length = math.floor(len(data)*7.0/10.0)
	return data[:], data[:]

def f1(x):
	return float(x.num_tubes)

def f2(x):
	return float(x.length)

def f3(x):
	return float(x.width)

def f4(x):
	return float(x.height)

def f5(x):
	return float(x.mass)

def f6(x):
	return float(x.num_gasbox)

def f7(x):
	if x.customer not in customers:
		customers.append(x.customer)
	return float(customers.index(x.customer)) 

def f8(x):
	return float(x.peak_volume)

def f9(x):
	return float(x.lifetime_volume)

def f10(x):
	return float(x.created) - 2014

def generate_features(x, features_used):
	output = []

	if "number of tubes" in features_used:
		output.append(f1(x))
	if "length" in features_used:
		output.append(f2(x))
	if "width" in features_used:
		output.append(f3(x))
	if "height" in features_used:
		output.append(f4(x))
	if "mass" in features_used:
		output.append(f5(x))
	if "number of gas boxes" in features_used:
		output.append(f6(x))
	if "customer" in features_used:
		output.append(f7(x))
	if "peak volume" in features_used:
		output.append(f8(x))
	if "lifetime volume" in features_used:
		output.append(f9(x))
	if "year" in features_used:
		output.append(f10(x))

	return output

def features(data, features_used):
	return np.array([generate_features(x, features_used) for x in data])

def labels(data):
	return np.array([float(x.final_price) for x in data])

def features_labels(data, features_used):
	return features(data, features_used), labels(data)