from sklearn.utils import resample
import sklearn.metrics as sk_metrics
import model.data_input as data_input, model.features as features, model.metrics as metrics, model.results as results, model.save as save
from random import shuffle
import numpy as np
from model.ml_models import *

features_used = data_input.features_used
INPUT_FILE = "model/test_data.csv"

# number of bootstrap models
num_iterations = 100

def get_quote(sample, clfs, decision_tree):
	# run cooler through first level
	tree_test = np.zeros(len(clfs))
	for k in range(len(clfs)):
		tree_test[k] = clfs[k].predict( sample.reshape(1, -1) )

	# run cooler through second level
	pred = decision_tree.predict( tree_test.reshape(1, -1) )

	# get the lower and upper limits of the confidence interval
	lower, upper = metrics.c_interval( tree_test, pred )

	return pred, lower, upper

def predict_cooler(program_dict, sim_model, num_results):
	
	# load latest model and data
	pred_model = save.get_version(save.get_prefix("model")) - 1
	clfs, decision_tree, model_type, parameter, _ = save.load("model", pred_model)
	data, encoders, averages = save.load("data")

	# create cooler
	cooler = data_input.create_program(program_dict, encoders, averages)
	sample = features.features([cooler], encoders, features_used)

	# get predictions
	quote, lower, upper = get_quote(sample, clfs, decision_tree)

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

	# split into training and testing set
	x_train, x_test = features.split_data(x)
	y_train, y_test = features.split_data(y)

	# prepare for bootstrapping
	n_size = len(x_train)
	test_size = len(x_test)
	indices = list(range(n_size))
	clfs = []
	scores = []

	# second level model 
	second_level = tree.DecisionTreeRegressor()
	tree_train = np.zeros( (num_iterations, n_size) )

	# num_iterations is the number of bootstrapped instances to create
	for instance in range(num_iterations):

		# make bootstrap samples indices
		train_indices = resample(indices, n_samples=n_size)

		# prepare train and test sets
		x_bs = x[train_indices]
		y_bs = y[train_indices].reshape(-1,1)

		# train model
		clf = globals()[model_type](parameter)
		clf.fit(x_bs, y_bs)

		# training data for second level model
		tree_train[instance] = clf.predict(x_train).reshape(n_size)

		# keep important values for next iteration
		clfs.append(clf)

	# training second level model
	tree_train = np.transpose(tree_train)
	second_level.fit( tree_train, y_train )

	# calculate a baseline
	median = [metrics.median(y_train)] * test_size
	base = sk_metrics.mean_absolute_error(y_test, median)

	# calculate the metrics
	y_ensemble = np.zeros( (3, test_size ) )

	# for each cooler in the test set
	for idx in range(test_size):
		pred, lower, upper = get_quote(x_test[idx], clfs, second_level)

		# save these values
		y_ensemble[0][idx] = pred
		y_ensemble[1][idx] = lower
		y_ensemble[2][idx] = upper


	# calculate comparators
	comparators = metrics.get_comparators(y_test, y_ensemble)

	# save models to predict coolers
	save.update("model", [clfs, second_level, model_type, parameter, comparators])

	return base, comparators['mean-absolute-error']


def get_models(trans):
	prefix = save.get_prefix("model")
	versions = save.get_version(prefix)
	models = []

	for v in range(versions-1):
		_, _, model_type, parameter, _ = save.load("model", v+1)
		new_model = {}
		new_model['id'] = v+1
		new_model['name'] = trans[model_type]
		if parameter != "":
			new_model['name'] += ", " + parameter
		models.append(new_model)

	return models
		

def run_all():
	prefix = save.get_prefix("model")
	versions = save.get_version(prefix)
	
	display = []

	for v in range(versions-1):
		_, _, model_type, parameter, comparators = save.load("model", v+1)
		display.append([model_type, parameter, comparators])

	return display

def create_data(input_file):
	data = data_input.parse_data(input_file)
	data, encoders = data_input.int_encode(data)
	averages = data_input.get_averages(data)
	shuffle(data)

	return data, encoders, averages

def update_data():
	data, encoders, averages = create_data(INPUT_FILE)
	save.update("data", [data, encoders, averages])

def add_cooler(program):
	# TURN PROGRAM INTO CSV LINE ITEM
	csv_line = data_input.create_csv_item(program)

	# ADD COOLER TO EXCEL
	data_input.add_to_csv(INPUT_FILE, csv_line)

	# UPDATE DATA
	update_data()

	return "SUCCESS"

def clean():
	save.clean()
