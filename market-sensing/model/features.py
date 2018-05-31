from random import shuffle
import math
import numpy as np

customers = []
regions = []
tube_types = []
car_types = []
bypass_valves = []

def split_data(data):
	shuffle(data)
	length = math.floor(len(data)*7.0/10.0)
	return data[:], data[:]

def num_tubes(x):
	return float(x.data['num_tubes'])

def tube_type(x):
	value = x.data['tube_type']
	if value not in tube_types:
		tube_types.append(value)
	return float(tube_types.index(value)) 

def length(x):
	return float(x.data['length'])

def width(x):
	return float(x.data['width'])

def height(x):
	return float(x.data['height'])

def mass(x):
	return float(x.data['mass'])

def bypass_valve(x):
	value = x.data['bypass_valve']
	if value not in bypass_valves:
		bypass_valves.append(value)
	return float(bypass_valves.index(value)) 

def num_brackets(x):
	return float(x.data['num_brackets'])

def num_spigots(x):
	return float(x.data['num_spigots'])


def peak_volume(x):
	return float(x.data['peak_volume'])

def lifetime_volume(x):
	return float(x.data['lifetime_volume'])

def customer(x):
	value = x.data['customer']
	if value not in customers:
		customers.append(value)
	return float(customers.index(value)) 

def car_type(x):
	value = x.data['car_type']
	if value not in tube_types:
		tube_types.append(value)
	return float(car_types.index(value))

def region(x):
	value = x.data['region']
	if value not in tube_types:
		tube_types.append(value)
	return float(tube_types.index(value)) 

def sop_year(x):
	return float(x.data['sop_year']) - 2014


def generate_features(x, features_used):
	output = []

	if "num_tubes" in features_used:
		output.append(num_tubes(x))
	if "tube_type" in features_used:
		output.append(tube_type(x))
	if "length" in features_used:
		output.append(length(x))
	if "width" in features_used:
		output.append(width(x))
	if "height" in features_used:
		output.append(height(x))
	if "mass" in features_used:
		output.append(mass(x))
	if "bypass_valve" in features_used:
		output.append(bypass_valve(x))	
	if "num_brackets" in features_used:
		output.append(num_brackets(x))	
	if "num_spigots" in features_used:
		output.append(num_spigots(x))
	if "peak_volume" in features_used:
		output.append(peak_volume(x))
	if "lifetime_volume" in features_used:
		output.append(lifetime_volume(x))
	if "customer" in features_used:
		output.append(customer(x))
	if "car_type" in features_used:
		output.append(car_type(x))				
	if "sop_year" in features_used:
		output.append(sop_year(x))
	if "region" in features_used:
		output.append(region(x))
	return output

def features(data, features_used):
	return np.array([generate_features(x, features_used) for x in data])

def labels(data):
	return np.array([float(x.data['final_price']) for x in data])

def features_labels(data, features_used):
	return features(data, features_used), labels(data)