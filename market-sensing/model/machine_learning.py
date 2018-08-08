from sklearn.utils import resample
import sklearn.metrics as sk_metrics
import model.data_input as data_input, model.features as features, model.metrics as metrics
import model.results as results, model.save as save, model.similarity as similarity
from random import shuffle
import numpy as np
from model.ml_models import *
from model.config import *

features_used = data_input.features_used
INPUT_FILE = "model/test_data.csv"

# number of bootstrap models
num_iterations = 100

def predict(program_dict, sim_model, num_results):
	
	# load latest model and data
	pred_model = save.get_version(save.get_prefix("model")) - 1
	clfs, decision_tree, model_type, parameter, _ = save.load("model", pred_model)
	data, encoders, averages = save.load("data")

	# create cooler
	cooler = data_input.create_program(program_dict, encoders, averages)
	sample = features.features([cooler], encoders)

	# get predictions
	quote, lower, upper = results.get_quote(sample, clfs, decision_tree)

	# find similar coolers
	scores = results.similarity(cooler, data, sim_model)

	# display correctly
	similar_list = results.sort_and_display(data, scores, num_results, encoders)

	return quote, lower, upper, similar_list


def create(model_type, parameter):
	# load latest data
	data, encoders, averages = save.load("data")
	normalized = [(data_input.replace_blanks(item, averages)) for item in data]

	# generate features
	x, y = features.features_labels(normalized, encoders)

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
	# get prefix of model files
	prefix = save.get_prefix("model")

	#get number of versions with this prefix
	versions = save.get_version(prefix)

	# return name, version number, and parameter of each model
	models = []
	for v in range(versions-1):
		_, _, model_type, parameter, _ = save.load("model", v+1)

		new_model = {
			'id': v+1,
			'name' = trans[model_type]
		}

		# add parameter if it exists
		if parameter != "":
			new_model['name'] += ", " + parameter

		# append this model to the output
		models.append(new_model)

	return models
		

def run():
	prefix = save.get_prefix("model")
	versions = save.get_version(prefix)
	
	display = []

	for v in range(versions-1):
		_, _, model_type, parameter, comparators = save.load("model", v+1)
		display.append([model_type, parameter, comparators])

	return display

def data():
	input_file = "model/test_data.csv"

	data = data_input.parse_data(input_file)
	data, encoders = similarity.int_encode(data)
	averages = similarity.get_averages(data)
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
