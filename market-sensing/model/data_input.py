parameters = ['use', 'created', 'customer', 'num_tubes', 'length', 'width', 'height', 'mass',
		'num_gasbox', 'peak_volume', 'lifetime_volume', 'region', 'final_price']

def if_empty(value):
	if value == "":
		return "0"
	else:
		return value

def clean(value):
	value = if_empty(value)
	value = value.lower()
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

		for i in range(len(csv_order)):
			col = csv_order[i]
			program_dict[col] = split[i]

		output.append(Program(program_dict))

	return output


def clean_data(items):
	output = []
	for x in items:
		if x.data['use'] == "yes":
			output.append(x)
	return output

def create_program(program_dict):
	return Program(program_dict)

if __name__ == "__main__":
	print("Start")
	parse_data("data.csv")
	print("Finish")
