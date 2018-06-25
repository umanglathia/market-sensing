from sklearn import linear_model, svm, neighbors, gaussian_process, tree, ensemble, neural_network
from sklearn.utils import resample
import model.data_input as data_input, model.features as features, model.metrics as metrics, model.results as results, model.save as save
from random import shuffle
import numpy as np
from matplotlib import pyplot

features_used = data_input.features_used

# number of bootstrap models
num_interations = 100

def predict_cooler(program_dict, sim_model, num_results):
	# load latest model and data
	pred_model = save.get_version(save.get_prefix("model")) - 1
	clfs, model_type, parameter = save.load("model", pred_model)
	data, encoders, averages = save.load("data")

	# create cooler
	cooler = data_input.create_program(program_dict, encoders, averages)
	print(cooler.data['tube_type'])

	# run on all models
	quotes = []
	for clf in clfs:
		quote = results.get_quote(cooler, clf, features_used, encoders)
		quotes.append(quote)

	# get 95% confidence interval
	lower, upper = metrics.c_interval(quotes)
	quote = metrics.median(quotes)

	# find similar coolers
	scores = results.similarity(cooler, data, features_used, sim_model)

	# display correctly
	similar_list = results.sort_and_display(data, scores, num_results, encoders)

	return quote, lower, upper, similar_list

def create_model(model_type, parameter):
	# load latest data
	data, encoders, averages = save.load("data")
	normalized = data_input.normalize_data(data, averages)

	# generate features
	x, y = features.features_labels(normalized, encoders, features_used)

	# prepare for bootstrapping
	n_size = len(x)
	indices = list(range(len(x)))
	clfs = []
	scores = []

	for i in range(num_interations):

		# make bootstrap samples indices
		train_indices = resample(indices, n_samples=n_size)
		test_indices = np.array([x for x in indices if x not in train_indices])

		# prepare train and test sets
		x_train = x[train_indices]
		y_train = y[train_indices]
		x_test = x[test_indices]
		y_test = y[test_indices]

		# train model
		clf = globals()[model_type](parameter)
		clf.fit(x_train, y_train)

		# calculate a baseline
		mean = [float(sum(y_test))/len(y_test)]*len(y_test)
		base = metrics.get_accuracy(mean, y_test)

		# evaluate model
		y_pred = clf.predict(x_test)
		score = metrics.get_accuracy(y_pred, y_test)

		# keep important values for next iteration
		clfs.append(clf)
		scores.append(score)

	lower, upper = metrics.c_interval(scores)
	return clfs, [base, lower, upper]

def update_model(model_type, parameter):
	clfs, accuracy = create_model(model_type, parameter)
	save.update("model", [clfs, model_type, parameter])
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
	data, encoders, averages = create_data("model/test_data2.csv")
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