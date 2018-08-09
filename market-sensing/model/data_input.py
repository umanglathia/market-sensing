from model.config import *

# Program object, used for input
class Program:
	def __init__(self, program_dict):
		self.data = {}
		self.normalized = []
		for x in parameters:
			self.data[x] = clean(program_dict[x])


# clean values for comparison
def clean(value):
	value = value.lower()

	if value == "" or value == " ":
		value = None

	return value


def parse_data(input_file):
	# read in csv file
	file = open(input_file, encoding="latin1")
	lines = file.readlines()
	data = []

	# for each cooler in the file
	for line in lines[1:]:

		# create a Program object for it
		item_dict = {}
		split = line.split(",")

		# turn list into dictionary
		for i, col in enumerate(parameters):
			item_dict[col] = split[i]

		# turn dictionary into object
		program = Program(item_dict)

		# only use it if 'use' is 'yes'
		if program.data['use'] == "yes":
			data.append(program)

	return data

def encode_parameter(items, parameter):
	unique = [None]
	for i in range(len(items)):
		value = items[i].data[parameter]
		if value not in unique:
			unique.append(value)
		items[i].data[parameter] = int(unique.index(value))

	return items, unique

def int_encode(data):
	encoders = {}
	for parameter in features_used:
		if parameter not in numerical:
			data, encoder = encode_parameter(data, parameter)
			encoders[parameter] = encoder

	return data, encoders

def encode_quote(item, encoders):
	for attr in features_used:
		if attr not in numerical:
			item.data[attr] = encoders[attr].index(item.data[attr])

	return item


def replace_blanks(item, averages):
	# replace all blank values
	for attr in features_used:
		# if the attribute is numerical, the null value is None
		if attr in numerical and item.data[attr] == None:
			item.data[attr] = averages[attr]
			item.normalized.append(attr)

		# if the attribute is not numerical, the null value is 0
		if attr not in numerical and item.data[attr] == 0:
			item.data[attr] = averages[attr]
			item.normalized.append(attr)	

	return item


def create_program(item_dict, encoders, averages):
	# create program object
	item = Program(item_dict)

	# turn strings into integers
	item = encode_quote(item, encoders)

	# replace values that are empty with the majority
	item = replace_blanks(item, averages)

	return item

def create_csv_item(program_dict):
	output = []
	for attr in parameters:
		output.append(program_dict[attr])

	return (',').join(output)

def add_to_csv(file, csv_line):
	f = open(file, "a", encoding="latin1")
	f.write(csv_line + "\n")
	f.close
