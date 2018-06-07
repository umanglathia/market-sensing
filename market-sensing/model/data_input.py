from collections import Counter
import math

parameters = ['program_number', 'use', 'num_tubes', "tube_type", 'length', 'width', 'height', 'mass',
		'bypass_valve', 'num_brackets', 'spigot_type', 'num_gasboxes', 'peak_volume', 'lifetime_volume',
		'customer', 'car_type', 'region', 'sop_year', 'bw_quote', 'status', 'final_price']

numerical = ['num_tubes', 'length', 'width', 'height', 'mass', 'num_brackets', 'num_gasboxes',
		'peak_volume', 'lifetime_volume', 'sop_year']

def if_empty(value):
	if value == "":
		return None
	else:
		return value

def clean(value):
	value = value.lower()
	value = if_empty(value)
	return value

def clean_data(items):
	output = []
	for x in items:
		if x.data['use'] == "yes":
			output.append(x)

	return output

	#return item in items if item.data['use'] == "yes"

class Program:
	def __init__(self, program_dict):
		self.data = {}
		self.normalized = []
		for x in parameters:
			self.data[x] = clean(program_dict[x])

def parse_data(input_file):
	file = open(input_file, encoding="latin1")
	lines = file.readlines()
	output = []

	for line in lines[1:]:
		program_dict = {}
		split = line.split(",")

		for i, col in enumerate(parameters):
			program_dict[col] = split[i]

		output.append(Program(program_dict))

	return output

def get_averages(items):
	output = {}

	for attr in parameters:
		if attr in numerical:
			numerator = sum(float(item.data[attr]) for item in items if item.data[attr] != None)
			denominator = sum(1 for item in items if item.data[attr] != None)
			if denominator == 0:
				denominator = 1
			output[attr] = numerator/denominator

		else:
			values = Counter()
			for item in items:
				if item.data[attr] != None:
					values[ item.data[attr] ] += 1

			output[attr] = values.most_common()[0][0]

	return output

def get_stdevs(items, averages):
	output = {}

	for attr in parameters:
		if attr in numerical:
			numerator = sum( (float(item.data[attr]) - averages[attr])**2 for item in items if item.data[attr] != None )
			denominator = sum(1 for item in items if item.data[attr] != None)
			if denominator == 0:
				denominator = 1
			output[attr] = math.sqrt( numerator / denominator )

		else:
			output[attr] = ""

	return output

def get_r2(features_used):
	output = {}

	for attr in features_used:
		if attr in numerical:
			output[attr] = 1

		else:
			output[attr] = .75

	return output


def normalize_item(item, averages):
	for attr in parameters:
		if item.data[attr] == None:
			item.data[attr] = averages[attr]
			item.normalized.append(attr)

	return item

def normalize_data(items):

	averages = get_averages(items)
	for i in range(len(items)):
		items[i] = normalize_item(items[i], averages)

	return items

def create_program(program_dict, data):
	program = Program(program_dict)
	averages = get_averages(data)
	return normalize_item(program, averages)
