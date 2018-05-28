from sklearn import linear_model, svm
import numpy as np
import data_input, features, metrics
import dill as pickle
import os

all_features =  ["use", "year", "customer", "number of tubes", "length", "width", "height", "mass", "number of gas boxes", "peak volume", "lifetime volume", "final price"]
features_used = ["number of tubes", "length", "width", "height", "mass", "customer", "peak volume", "lifetime volume", "year"]

def create_model():
	items = data_input.parse_data("test_data.csv")
	data = data_input.clean_data(items)

	train, test = features.split_data(data)
	train_x, train_y = features.features_labels(train, features_used)
	test_x, test_y = features.features_labels(test, features_used)

	clf = linear_model.LinearRegression()
	clf.fit(train_x, train_y)

	return clf

def run_model(clf):

	while(True):
		print("\n")
		boolean = input("Would you like to find the market value of a tube? (y/n): ")
		
		if boolean == "n":
			exit()

		if boolean == "y":
			inputs = [""]*len(all_features)

			for i, f in enumerate(all_features):
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
	clf = create_model()

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