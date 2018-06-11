from sklearn import linear_model, svm, neighbors, gaussian_process, tree, ensemble, neural_network
import model.data_input as data_input, model.features as features, model.metrics as metrics, model.results as results, model.save as save
from random import shuffle
import numpy as np

features_used = ['num_tubes', "tube_type", 'length', 'width', 'height', 'mass', 'bypass_valve',
		'num_brackets', 'spigot_type', 'num_gasboxes', 'peak_volume', 'lifetime_volume', 'customer',
		'market_segment', 'market', 'sop_year']

def predict_cooler(program_dict, sim_model, num_results, pred_model):
	clf, model_type, parameter = save.load("model", pred_model)
	data, encoders, averages = save.load("data")
	cooler = data_input.create_program(program_dict, encoders, averages)
	quote = results.get_quote(cooler, clf, features_used, encoders)
	scores = results.similarity(cooler, data, features_used, sim_model)
	similar_list = results.sort_and_display(data, scores, num_results, encoders)

	return quote, similar_list

def create_model(model_type, parameter):
	data, encoders, averages = save.load("data")
	normalized = data_input.normalize_data(data, averages)

	x, y = features.features_labels(normalized, encoders, features_used)
	train_x, test_x = features.split_data(x)
	train_y, test_y = features.split_data(y)

	clf = globals()[model_type](parameter)
	clf.fit(train_x, train_y)

	mean = [float(sum(test_y))/len(test_y)]*len(test_y)
	acc1 = metrics.get_accuracy(mean, test_y)

	y_pred = clf.predict(test_x)
	acc2 = metrics.get_accuracy(y_pred, test_y)
	
	return clf, [acc1, acc2]

def update_model(model_type, parameter):
	clf, accuracy = create_model(model_type, parameter)
	save.update("model", [clf, model_type, parameter])
	return accuracy

def get_models():
	prefix = save.get_prefix("model")
	versions = save.get_version(prefix)
	models = []

	for v in range(versions-1):
		_, model_type, parameter = save.load("model", v+1)
		new_model = {}
		new_model['id'] = v+1
		new_model['name'] = model_type.capitalize()
		if parameter != "":
			new_model['name'] += ", " + parameter
		models.append(new_model)

	return models
		

def run_all():
	prefix = save.get_prefix("model")
	versions = save.get_version(prefix)

	data, encoders, averages = save.load("data")
	normalized = data_input.normalize_data(data, averages)
	_, test = features.split_data(normalized)
	test_x, test_y = features.features_labels(test, encoders, features_used)
	accuracy = []

	for v in range(versions-1):
		clf, model_type, parameter = save.load("model", v+1)
		y_pred = clf.predict(test_x)
		acc = metrics.get_accuracy(y_pred, test_y)

		diff = y_pred - test_y

		accuracy.append([model_type, parameter, acc, diff])

	return accuracy, test_y

def create_data(input_file):
	data = data_input.parse_data(input_file)
	data, encoders = data_input.int_encode(data)
	averages = data_input.get_averages(data)
	shuffle(data)

	return data, encoders, averages

def update_data():
	data, encoders, averages = create_data("model/test_data.csv")
	save.update("data", [data, encoders, averages])

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
	split = parameter.split(',')
	while len(split) < 3:
		split.append("")
	if split[0] == "":
		split[0] = 'ls'
	if split[1] == "":
		split[1] = 0.1
	if len(split) <= 2 or split[2] == "":
		split[2] = 100
	return ensemble.GradientBoostingRegressor(loss=split[0], )

def mlpregressor(parameter):
	return neural_network.MLPRegressor()