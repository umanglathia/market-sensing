from sklearn import linear_model, svm
import numpy as np
import model.data_input as data_input
import model.features as features
import model.metrics as metrics
import model.results as results
import model.save as save
import copy

features_used = ['num_tubes', "tube_type", 'length', 'width', 'height', 'mass', 'bypass_valve',
		'num_brackets', 'spigot_type', 'num_gasboxes', 'peak_volume', 'lifetime_volume', 'customer',
		'car_type', 'region', 'sop_year']

def load_latest_model():
	return save.load_latest_model()

def predict_cooler(program_dict, model, num_results):
	clf, data = load_latest_model()
	cooler = data_input.create_program(program_dict, data)
	quote = results.get_quote(cooler, clf, features_used)
	scores = results.similarity(cooler, data, features_used, model)
	similar_list = results.sort_and_display(data, scores, num_results)

	return quote, similar_list

def create_model(input_file):
	items = data_input.parse_data(input_file)
	data = data_input.clean_data(items)
	save_data = copy.deepcopy(data)
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
	
	return clf, save_data, [acc1, acc2]

def clean():
	save.clean()

def update():
	clf, programs, accuracy = create_model("model/test_data.csv")
	return save.update(clf, programs, accuracy)