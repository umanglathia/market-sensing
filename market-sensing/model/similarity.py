from model.config import *

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