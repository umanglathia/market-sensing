from model.config import *
from collections import Counter
import math
import model.data_input as data_input

numerical = data_input.numerical
dropoff = 0.1
x_zero = 1.0
a = dropoff*x_zero/(x_zero - dropoff)
b = dropoff/(dropoff - x_zero)

def get_r2():
	output = {}

	for attr in features_used:
		if attr in numerical:
			output[attr] = 1

		else:
			output[attr] = .75

	return output

def get_averages(items):
	averages = {}
	for attr in features_used:
		if attr in numerical:
			numerator = sum(float(item.data[attr]) for item in items if item.data[attr] != None)
			denominator = max(sum(1 for item in items if item.data[attr] != None), 1)
			averages[attr] = numerator/denominator

		else:
			values = Counter()
			for item in items:
				if item.data[attr] != None:
					values[ item.data[attr] ] += 1

			averages[attr] = values.most_common()[0][0]

	return averages

def get_stdevs(items, averages):
	output = {}

	for attr in features_used:
		if attr in numerical:
			numerator = sum( (float(item.data[attr]) - averages[attr])**2 for item in items if item.data[attr] != None )
			denominator = sum(1 for item in items if item.data[attr] != None)
			if denominator == 0:
				denominator = 1
			output[attr] = math.sqrt( numerator / denominator )

		else:
			output[attr] = ""

	return output

def get_scores(cooler, data, model):
	scores = [0]*len(data)

	averages = get_averages(data)
	stdevs = get_stdevs(data, averages)
	r2 = get_r2()

	for i, item in enumerate(data):
		if item.data['use'] == 'yes':
			scores[i] = globals()[model](cooler, item, averages, stdevs, r2)

	return scores

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

def norm_0(cooler, item, averages, stdevs, r2):
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

def euclidean(cooler, item, averages, stdevs, r2):
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

def manhattan(cooler, item, averages, stdevs, r2):
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

def cosine(cooler, item, averages, stdevs, r2):
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