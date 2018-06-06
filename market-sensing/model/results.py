import model.features as features
import model.data_input as data_input
from sklearn import linear_model, svm
import numpy as np
import random

NUM_TO_DISPLAY = 5
SCORING = "manhattan"
numerical = data_input.numerical
dropoff = 0.1
x_zero = 0.5
a = dropoff*x_zero/(x_zero - dropoff)
b = dropoff/(dropoff - x_zero)


def get_quote(cooler, clf, features_used):
	x, y = features.features_labels([cooler], features_used)
	quote = round(clf.predict(x)[0], 2)

	return quote

def consider(cooler, item, attr, averages):
	if cooler.data[attr] == averages[attr]:
		return False
	if cooler.data[attr] == " ":
		return False
	if item.data[attr] == averages[attr]:
		return False
	if item.data[attr] == None:
		return False

	return True

def quantize(cooler, attr, maxes, averages):
	return (float(cooler.data[attr]) - averages[attr])/(maxes[attr] - averages[attr])

def penalty(c, x):
	if abs(c - x) <= dropoff:
		return 1
	if abs(c - x) >= x_zero:
		return 0
	return a/abs(c - x) + b

def norm_0(cooler, item, features_used, averages):
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

def euclidean(cooler, item, features_used):
	return 0

def manhattan(cooler, item, features_used, averages, maxes):
	score = 0.0
	total = 0.0
	for attr in features_used:
		if consider(cooler, item, attr, averages):
			if attr in numerical:
				total += 1
				if attr in numerical:
					c = quantize(cooler, attr, maxes, averages)
					x = quantize(item, attr, maxes, averages)

					if attr == "num_tubes":
						print(c, x, penalty(c,x))
					score += penalty(c, x)

			else:
				total += .75
				if cooler.data[attr] == item.data[attr]:
					score += .75
				
	if total == 0:
		total = 1

	return float(score)/total

def cosine(cooler, item, features_used):
	return 0

def score(cooler, item, features_used, averages, maxes):
	if SCORING == "norm_0":
		return norm_0(cooler, item, features_used, averages)
	if SCORING == "euclidean":
		return euclidean(cooler, item, features_used, averages)
	if SCORING == "manhattan":
		return manhattan(cooler, item, features_used, averages, maxes)
	if SCORING == "cosine":
		return cosine(cooler, item, features_used, averages)

def similarity(cooler, data, features_used):
	scores = [0]*len(data)
	averages = data_input.get_averages(data)
	maxes = data_input.get_max(data)
	for i, item in enumerate(data):
		scores[i] = score(cooler, item, features_used, averages, maxes)
	return scores

def format(item):
	item.display = {}
	for attr in data_input.parameters:
		if item.data[attr] == None:
			item.data[attr] = " "
		item.display[attr] = item.data[attr].title()

		if item.display[attr] != " ":
			if attr in ['length', 'width', 'height']:
				item.display[attr] += "mm"
			if attr in ['mass']:
				item.display[attr] += "g"
			if item.display[attr] in ["Hkmc", "Vcc", "Eu"]:
				item.display[attr] = item.display[attr].upper()
			if item.display[attr] == "North America":
				item.display[attr] = "NA"
			if item.display[attr] == "South America":
				item.display[attr] = "SA"

	return item

def sort_and_display(data, scores):
	idx = np.argsort(scores)
	ascending = idx[::-1]
	scores = np.array(scores)[ascending]
	data = np.array(data)[ascending]

	for i in range(NUM_TO_DISPLAY):
		data[i] = format(data[i])

	return zip(data[:NUM_TO_DISPLAY], scores[:NUM_TO_DISPLAY])