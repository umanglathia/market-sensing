import math
import numpy as np

customers = []
markets = []
tube_types = []
market_segments = []
bypass_valves = []
spigot_types = []

def split_data(data):
	length = math.floor(len(data)*7.0/10.0)
	return data[:length], data[length+1:]

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

def spigot_type(x):
	value = x.data['spigot_type']
	if value not in spigot_types:
		spigot_types.append(value)
	return float(spigot_types.index(value)) 

def num_gasboxes(x):
	return float(x.data['num_gasboxes'])

def peak_volume(x):
	return float(x.data['peak_volume'])

def lifetime_volume(x):
	return float(x.data['lifetime_volume'])

def customer(x):
	value = x.data['customer']
	if value not in customers:
		customers.append(value)
	return float(customers.index(value)) 

def market_segment(x):
	value = x.data['market_segment']
	if value not in market_segments:
		market_segments.append(value)
	return float(market_segments.index(value))

def market(x):
	value = x.data['market']
	if value not in markets:
		markets.append(value)
	return float(markets.index(value)) 

def sop_year(x):
	return float(x.data['sop_year']) - 2014


def generate_features(x, features_used):
	output = []

	for feature in features_used:
		output.append(globals()[feature](x))

	return output

def features(data, features_used):
	return np.array([generate_features(x, features_used) for x in data])

def labels(data):
	return np.array([float(x.data['final_price']) for x in data])

def features_labels(data, features_used):
	return features(data, features_used), labels(data)