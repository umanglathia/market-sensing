from random import shuffle
import math
import numpy as np

customers = []
regions = []
tube_types = []
car_types = []

def split_data(data):
	shuffle(data)
	length = math.floor(len(data)*7.0/10.0)
	return data[:], data[:]

def num_tubes(x):
	return float(x.data['num_tubes'])

def length(x):
	return float(x.data['length'])

def width(x):
	return float(x.data['width'])

def height(x):
	return float(x.data['height'])

def mass(x):
	return float(x.data['mass'])

def num_gasbox(x):
	return float(x.data['num_gasbox'])

def customer(x):
	value = x.data['customer']
	if value not in tube_types:
		tube_types.append(value)
	return float(customers.index(value)) 

def peak_volume(x):
	return float(x.data['peak_volume'])

def lifetime_volume(x):
	return float(x.data['lifetime_volume'])

def sop_year(x):
	return float(x.data['created'])

def region(x):
	value = x.data['region']
	if value not in tube_types:
		tube_types.append(value)
	return float(customers.index(value)) 

def tube_type(x):
	value = x.data['tube_type']
	if value not in tube_types:
		tube_types.append(value)
	return float(customers.index(value)) 

def car_type(x):
	value = x.data['car_type']
	if value not in tube_types:
		tube_types.append(value)
	return float(customers.index(value)) 

def num_spigots(x):
	return float(x.data['num_spigots'])

def num_brackets(x):
	return float(x.data['num_brackets'])


def generate_features(x, features_used):
	output = []

	if "number of tubes" in features_used:
		output.append(num_tubes(x))
	if "length" in features_used:
		output.append(length(x))
	if "width" in features_used:
		output.append(width(x))
	if "height" in features_used:
		output.append(height(x))
	if "mass" in features_used:
		output.append(mass(x))
	if "number of gas boxes" in features_used:
		output.append(num_gasbox(x))
	if "customer" in features_used:
		output.append(customer(x))
	if "peak volume" in features_used:
		output.append(peak_volume(x))
	if "lifetime volume" in features_used:
		output.append(lifetime_volume(x))
	if "sop year" in features_used:
		output.append(sop_year(x))
	if "region" in features_used:
		output.append(region(x))
	if "tube type" in features_used:
		output.append(tube_type(x))
	if "car type" in features_used:
		output.append(car_type(x))
	if "bypass valve" in features_used:
		output.append(bypass_valve(x))
	if "number of spigots" in featuers_used:
		output.append(num_spigots(x))
	if "number of brackets" in features_used:
		output.append(num_brackets(x))

	return output

def features(data, features_used):
	return np.array([generate_features(x, features_used) for x in data])

def labels(data):
	return np.array([float(x.data['final_price']) for x in data])

def features_labels(data, features_used):
	return features(data, features_used), labels(data)