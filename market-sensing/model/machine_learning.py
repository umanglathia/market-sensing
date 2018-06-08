from sklearn import linear_model, svm, neighbors, gaussian_process, tree, ensemble, neural_network
import model.data_input as data_input, model.features as features, model.metrics as metrics, model.results as results, model.save as save
from random import shuffle
import numpy as np

features_used = ['num_tubes', "tube_type", 'length', 'width', 'height', 'mass', 'bypass_valve',
		'num_brackets', 'spigot_type', 'num_gasboxes', 'peak_volume', 'lifetime_volume', 'customer',
		'market_segment', 'market', 'sop_year']

def predict_cooler(program_dict, model, num_results):
	clf = save.load("model")
	data = save.load("data")
	cooler = data_input.create_program(program_dict, data)
	quote = results.get_quote(cooler, clf, features_used)
	scores = results.similarity(cooler, data, features_used, model)
	similar_list = results.sort_and_display(data, scores, num_results)

	return quote, similar_list

def create_model(model_type, parameter):
	data = save.load("data")
	normalized = data_input.normalize_data(data)

	train, test = features.split_data(normalized)
	train_x, train_y = features.features_labels(train, features_used)
	test_x, test_y = features.features_labels(test, features_used)

	clf = globals()[model_type](parameter)
	clf.fit(train_x, train_y)

	mean = [float(sum(test_y))/len(test_y)]*len(test_y)
	acc1 = metrics.get_accuracy(mean, test_y)

	y_pred = clf.predict(test_x)
	acc2 = metrics.get_accuracy(y_pred, test_y)
	
	return clf, [acc1, acc2]


def run_all():
	prefix = save.get_prefix("model")
	versions = save.get_version(prefix)

	data = save.load("data")
	normalized = data_input.normalize_data(data)
	_, test = features.split_data(normalized)
	test_x, test_y = features.features_labels(test, features_used)
	accuracy = []

	for v in range(versions-1):
		clf = save.load("model", v+1)
		y_pred = clf.predict(test_x)
		acc = metrics.get_accuracy(y_pred, test_y)

		accuracy.append(acc)

	return accuracy

def update_model(model_type, parameter):
	clf, accuracy = create_model(model_type, parameter)
	save.update("model",clf)
	return accuracy

def create_data(input_file):
	items = data_input.parse_data(input_file)
	data = data_input.clean_data(items)
	shuffle(data)
	return data

def update_data():
	data = create_data("model/test_data.csv")
	save.update("data", data)

def clean():
	save.clean()

def least_squares(parameter):
	return linear_model.LinearRegression()

def ridge(parameter):
	return linear_model.Ridge()

def lasso(parameter):
	return linear_model.Lasso()

def elastic_net(parameter):
	return linear_model.ElasticNet()

def lasso_lars(parameter):
	return linear_model.LassoLars()

def perceptron(parameter):
	return linear_model.Perceptron()

def nearest_neighbor(parameter):
	return neighbors.KNeighborsRegressor()

def gpr(parameter):
	return gaussian_process.GaussianProcessRegressor()

def decision_tree(parameter):
	return tree.DecisionTreeRegressor()

def boosting(parameter):
	return ensemble.GradientBoostingRegressor()

def mlpregressor(parameter):
	return neural_network.MLPRegressor()