import model.features as features
import model.data_input as data_input
import model.metrics as metrics
from sklearn import linear_model, svm
import numpy as np
import random
import math

def get_quote(sample, clfs, decision_tree):
	# run cooler through first level
	tree_test = np.zeros(len(clfs))
	for k in range(len(clfs)):
		tree_test[k] = clfs[k].predict( sample.reshape(1, -1) )

	# run cooler through second level
	pred = decision_tree.predict( tree_test.reshape(1, -1) )

	# get the lower and upper limits of the confidence interval
	lower, upper = metrics.c_interval( tree_test, pred )

	return pred, lower, upper

def format(item, encoders):
	item.display = {}
	for attr in data_input.parameters:
		if attr in encoders:
			item.data[attr] = encoders[attr][item.data[attr]]
		if item.data[attr] == None:
			item.data[attr] = ""

		if item.display[attr] != "":
			if attr in ['length', 'width', 'height']:
				item.display[attr] += "mm"
			if attr in ['mass']:
				item.display[attr] += "g"

	return item

def sort_and_display(data, scores, num_results, encoders):
	idx = np.argsort(scores)
	ascending = idx[::-1]
	scores = np.array(scores)[ascending]
	data = np.array(data)[ascending]

	for i in range(num_results):
		data[i] = format(data[i], encoders)

	return zip(data[:num_results], scores[:num_results])