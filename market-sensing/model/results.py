import model.features as features
import model.data_input as data_input
from sklearn import linear_model, svm
import numpy as np
import random
import math

numerical = data_input.numerical
dropoff = 0.1
x_zero = 0.5
a = dropoff*x_zero/(x_zero - dropoff)
b = dropoff/(dropoff - x_zero)

def get_quote(cooler, clf, features_used, encoders):
	x = features.features([cooler], encoders, features_used)
	return clf.predict(x)[0]

def consider(cooler, item, attr):

	if attr in cooler.normalized:
		return False
	if cooler.data[attr] == " ":
		return False
	if attr in item.normalized:
		return False
	if item.data[attr] == None:
		return False
	if cooler.data[attr] == 0:
		return False

	return True

def quantize(cooler, attr, stdevs, averages):
	return (float(cooler.data[attr]) - averages[attr])/stdevs[attr]

def penalty(c, x):
	if abs(c - x) <= dropoff:
		return 1
	if abs(c - x) >= x_zero:
		return 0
	return a/abs(c - x) + b

def norm_0(cooler, item, features_used, averages, stdevs, r2):
	score = 0
	total = 0
	for attr in features_used:
		if consider(cooler, item, attr, averages):
			total += 1
			if cooler.data[attr] == item.data[attr]:
				score += 1

	if total == 0:
		total = 1

	return float(score)/total

def euclidean(cooler, item, features_used, averages, stdevs, r2):
	score = 0.0
	total = 0.0
	for attr in features_used:
		if consider(cooler, item, attr):
			if attr in numerical:
				total += (1*r2[attr])**2
				c = quantize(cooler, attr, stdevs, averages)
				x = quantize(item, attr, stdevs, averages)
				score += (penalty(c, x)*r2[attr])**2

			else:
				total += (1*r2[attr])**2
				if cooler.data[attr] == item.data[attr]:
					score += (1*r2[attr])**2
				
	if total == 0:
		total = 1

	return float(math.sqrt(score))/math.sqrt(total)

def manhattan(cooler, item, features_used, averages, stdevs, r2):
	score = 0.0
	total = 0.0
	for attr in features_used:
		if consider(cooler, item, attr):
			if attr in numerical:
				total += 1*r2[attr]
				c = quantize(cooler, attr, stdevs, averages)
				x = quantize(item, attr, stdevs, averages)
				score += penalty(c, x)*r2[attr]

			else:
				total += 1*r2[attr]
				if cooler.data[attr] == item.data[attr]:
					score += 1*r2[attr]
				
	if total == 0:
		total = 1


	return float(score)/total

def cosine(cooler, item, features_used, averages, stdevs, r2):
	score = 0.0
	magA = 0.0
	magB = 0.0
	for attr in features_used:
		if consider(cooler, item, attr):
			if attr in numerical:
				c = quantize(cooler, attr, stdevs, averages)
				x = quantize(item, attr, stdevs, averages)
				magA += (c*math.sqrt(r2[attr]))**2
				magB += (x*math.sqrt(r2[attr]))**2
				score += c*r2[attr]*x

			else:
				magA += (math.sqrt(r2[attr]))**2
				magB += (math.sqrt(r2[attr]))**2
				if cooler.data[attr] == item.data[attr]:
					score += r2[attr]
			
	if magA == 0:
		magA = 1
	if magB == 0:
		magB = 1

	return (score/(math.sqrt(magA)*math.sqrt(magB))+1.0)/2

def similarity(cooler, data, features_used, model):
	scores = [0]*len(data)

	averages = data_input.get_averages(data)
	stdevs = data_input.get_stdevs(data, averages)
	r2 = data_input.get_r2(features_used)

	for i, item in enumerate(data):
		scores[i] = globals()[model](cooler, item, features_used, averages, stdevs, r2)

	return scores

all_caps = ["HKMC", "VCC", "EU", "FCA", "HMC"]
accr = {
	"North America": "NA",
	"South America": "SA"
}

def format(item, encoders):
	item.display = {}
	for attr in data_input.parameters:
		if attr in encoders:
			item.data[attr] = encoders[attr][item.data[attr]]
		if item.data[attr] == None:
			item.data[attr] = ""
		item.display[attr] = item.data[attr].title()

		if item.display[attr] != "":
			if attr in ['length', 'width', 'height']:
				item.display[attr] += "mm"
			if attr in ['mass']:
				item.display[attr] += "g"
			if item.display[attr].upper() in all_caps:
				item.display[attr] = item.display[attr].upper()
			if item.display[attr] in accr:
				item.display[attr] = accr[ item.display[attr] ]

	return item

def sort_and_display(data, scores, num_results, encoders):
	idx = np.argsort(scores)
	ascending = idx[::-1]
	scores = np.array(scores)[ascending]
	data = np.array(data)[ascending]

	for i in range(num_results):
		data[i] = format(data[i], encoders)

	return zip(data[:num_results], scores[:num_results])