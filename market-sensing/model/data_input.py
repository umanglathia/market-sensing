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
	def __init__(self, split):
		self.use = clean(split[0])
		self.created = clean(split[1])
		self.customer = clean(split[2])
		self.num_tubes = clean(split[3])
		self.length = clean(split[4])
		self.width = clean(split[5])
		self.height = clean(split[6])
		self.mass = clean(split[7])
		self.num_gasbox = clean(split[8])
		self.peak_volume = clean(split[9])
		self.lifetime_volume = clean(split[10])
		self.final_price = clean(split[11])		

def parse_data(input_file):
	file = open(input_file, encoding="latin1")
	lines = file.readlines()
	output = []

	for line in lines[1:]:
		split = line.split(",")
		output.append(Program(split))

	return output


def clean_data(items):
	output = []
	for x in items:
		if x.use == "yes":
			output.append(x)

	return output

def create_program(split):
	return Program(split)

if __name__ == "__main__":
	print("Start")
	parse_data("data.csv")
	print("Finish")
