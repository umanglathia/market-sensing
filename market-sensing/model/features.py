import math
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def split_data(data):
	length = math.floor(len(data)*7.0/10.0)
	return data[:length], data[length+1:]

def numerical(x, attr):
	return float(x.data[attr])

def non_numerical(x, attr, length):
	output = np.zeros(length)
	output[ x.data[attr] ] = 1
	return output

def generate_features(x, encoders, features_used):
	output = []

	for feature in features_used:
		if feature in encoders:
			output.extend( non_numerical(x, feature, len(encoders[feature])))
		else:
			output.append( numerical(x, feature) )

	return output

def features(data, encoders, features_used):
	return np.array([generate_features(x, encoders, features_used) for x in data])

def labels(data):
	for x in data:
		print(x.data['final_price'])
		print(float(x.data['final_price']))
	return np.array([float(x.data['final_price']) for x in data])

def features_labels(data, encoders, features_used):
	return features(data, encoders, features_used), labels(data)