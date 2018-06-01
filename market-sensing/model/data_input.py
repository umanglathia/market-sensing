parameters = ['use', 'sop_year', 'customer', 'num_tubes', 'length', 'width', 'height', 'mass',
		'num_gasbox', 'peak_volume', 'lifetime_volume', 'region', 'final_price']

def if_empty(value):
	if value == "":
		return None
	else:
		return value

def clean(value):
	value = value.lower()
	value = if_empty(value)
	return value

class Program:
	def __init__(self, program_dict):
		self.data = {}

		for x in parameters:
			self.data[x] = clean(program_dict[x])

def parse_data(input_file):
	file = open(input_file, encoding="latin1")
	lines = file.readlines()
	output = []

	for line in lines[1:]:
		split = line.split(",")
		program_dict = {}

		for i in range(len(parameters)):
			col = parameters[i]
			program_dict[col] = split[i]

		output.append(Program(program_dict))

	return output

def get_averages(items):
	output = {}
	for attr in parameters:
		output[attr] = "0"

	numerical = ['num_tubes', 'sop_year', 'length', 'width', 'height', 'mass', 'num_gasbox',
	'peak_volume', 'lifetime_volume']

	for attr in numerical:
		numerator = sum(float(item.data[attr]) for item in items if item.data[attr] != None)
		output[attr] = numerator/len(items)

	return output

def normalize_item(item):
	for attr in parameters:
	if item.data[attr] == None:
		item.data[attr] = averages[attr]

	return item

def normalize_data(items):

	averages = get_averages(items)

	for i in range(len(items)):
		items[i] = normalize_item(i)

	return items

def clean_data(items):
	output = []
	for x in items:
		if x.data['use'] == "yes":
			output.append(x)

	return output

def create_program(program_dict, data):
	program = Program(program_dict)

	averages = get_averages(data)

	return normalize_data(program, averages)

if __name__ == "__main__":
	print("Start")
	parse_data("data.csv")
	print("Finish")
