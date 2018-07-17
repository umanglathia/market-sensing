import math
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from model.config import *

def split_data(data):
	length = math.floor(len(data)*7.0/10.0)
	return data[:length], data[length+1:]

def numerical(x, attr):
	return float(x.data[attr])

def non_numerical(x, attr, length):
	output = np.zeros(length)
	output[ x.data[attr] ] = 1
	return output

def generate_features(x, encoders):
	output = []

	for feature in features_used:
		if feature in encoders:
			output.extend( non_numerical(x, feature, len(encoders[feature])))
		else:
			output.append( numerical(x, feature) )

	return output

def features(data, encoders):
	return np.array([generate_features(x, encoders) for x in data])

def labels(data):
	return np.array([float(x.data['final_price']) for x in data])

def features_labels(data, encoders):
	return features(data, encoders), labels(data)