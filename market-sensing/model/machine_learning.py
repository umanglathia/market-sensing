from sklearn import linear_model, svm
import numpy as np
import model.data_input as data_input
import model.features as features
import model.metrics as metrics
import dill as pickle
import os

features_used = ["num_tubes", "length", "width", "height", "mass", "customer", "peak_volume", "lifetime_volume", "sop_year", "region"]

def load_latest_model():
	version = 1
	filename = "models/model_v1.pk"
	filename2 = "models/data_v1.pk"
	while True:
		version += 1
		temp_filename = "models/model_v" + str(version) + ".pk"
		temp_filename2 = "models/data_v" + str(version) + ".pk"
		if os.path.exists(temp_filename):
			filename = temp_filename
			filename2 = temp_filename2
		else:
			with open(filename, "rb") as f:
				clf = pickle.load(f)
				with open(filename2, "rb") as f2:
					data = pickle.load(f2)
					return clf, data



def get_quote(program_dict, clf, data):
	cooler = data_input.create_program(program_dict, data)
	x, y = features.features_labels([cooler], features_used)
	quote = round(clf.predict(x)[0], 2)

	return quote

def predict_cooler(program_dict):
	clf, data = load_latest_model()
	quote = get_quote(program_dict, clf, data)
	#scores = get_similarity(program_dict, data)
	similar_list = [1, 2, 3]

	return quote, similar_list

def create_model(input_file):
	items = data_input.parse_data(input_file)
	data = data_input.clean_data(items)
	normalized = data_input.normalize_data(data)

	train, test = features.split_data(normalized)
	train_x, train_y = features.features_labels(train, features_used)
	test_x, test_y = features.features_labels(test, features_used)

	clf = linear_model.Lasso(alpha = 0.2)
	clf.fit(train_x, train_y)

	median = [float(sum(test_y))/len(test_y)]*len(test_y)
	acc1 = metrics.get_accuracy(median, test_y)

	y_pred = clf.predict(test_x)
	acc2 = metrics.get_accuracy(y_pred, test_y)
	
	return clf, data, [acc1, acc2]

def clean():
	filename_to_delete = ""
	current_filename = "models/model_v1.pk"
	current_filename2 = "models/data_v1.pk"
	version = 1
	complete = False
	
	while not complete:
		version += 1
		temp_filename = "models/model_v" + str(version) + ".pk"
		temp_filename2 = "models/data_v" + str(version) + ".pk"

		if os.path.exists(temp_filename):
			os.remove(current_filename)
			os.remove(current_filename2)
			current_filename = temp_filename
			current_filename2 = temp_filename2
		
		else:
			os.rename(current_filename, "models/model_v1.pk")
			os.rename(current_filename2, "models/data_v1.pk")
			complete = True

	return

def update():
	clf, programs, accuracy = create_model("model/test_data.csv")
	version = 1
	found = False
	while not found:
		filename = "models/model_v" + str(version) + ".pk"
		data_file = "models/data_v" + str(version) + ".pk"
		if not os.path.exists(filename):
			found = True

		version += 1

	with open(filename, "wb") as file:
		pickle.dump(clf, file)

	with open(data_file, "wb") as file:
		pickle.dump(programs, file)

	return accuracy

def run_model(clf):

	while(True):
		print("\n")
		boolean = input("Would you like to find the market value of a tube? (y/n): ")
		
		if boolean == "n":
			exit()

		if boolean == "y":
			inputs = [""]*len(data_input.parmeters)

			for i, f in enumerate(data_input.parameters):
				if f in features_used:
					feature = input("Enter the " + f + ": ")
					inputs[i] = feature

			cooler = data_input.create_program(inputs)
			x, y = model.features_labels([cooler], features_used)
			quote = clf.predict(x)[0]

			print("The market value is $" + str(round(quote,2)))

def main():
	save = True
	run = False
	clf, data, acc = create_model("test_data.csv")

	if save == True:
		filename = "model_v3.pk"
		with open('../models/'+filename, 'wb') as file:
			pickle.dump(clf, file)

	if run == True:
		run_model(clf)

if __name__ == "__main__":
	print("Beginning Program")
	main()
	print("Ending Program")