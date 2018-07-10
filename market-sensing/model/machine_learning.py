from sklearn import linear_model, svm, neighbors, tree, ensemble, neural_network, kernel_ridge
from sklearn.utils import resample
import sklearn.metrics as sk_metrics
import model.data_input as data_input, model.features as features, model.metrics as metrics, model.results as results, model.save as save
from random import shuffle
import numpy as np
from matplotlib import pyplot

features_used = data_input.features_used

# number of bootstrap models
num_iterations = 100

def predict_cooler(program_dict, sim_model, num_results):
	# load latest model and data
	pred_model = save.get_version(save.get_prefix("model")) - 1
	clfs, model_type, parameter, _ = save.load("model", pred_model)
	data, encoders, averages = save.load("data")

	# create cooler
	cooler = data_input.create_program(program_dict, encoders, averages)

	# run on all models
	quotes = []
	for clf in clfs:
		quote = results.get_quote(cooler, clf, features_used, encoders)
		quotes.append(quote)

	# calculate the quote as the median prediction
	quote = np.mean(quotes)

	# get 95% confidence interval
	lower, upper = metrics.c_interval(quotes, median)

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
	indices = list(range(n_size))
	clfs = []
	scores = []

	# y_preds is an array of the predictions where each element is a list of the predictions
	# for that cooler in a model that doesn't train on that cooler
	y_preds = [ [] for i in range(n_size) ]

	# num_iterations is the number of bootstrapped instances to create
	for i in range(num_iterations):

		# make bootstrap samples indices
		train_indices = resample(indices, n_samples=n_size)
		test_indices = np.array([x for x in indices if x not in train_indices])

		# prepare train and test sets
		x_train = x[train_indices]
		y_train = y[train_indices].reshape(-1,1)
		x_test = x[test_indices]
		y_test = y[test_indices]

		# train model
		clf = globals()[model_type](parameter)
		clf.fit(x_train, y_train)

		# evaluate model
		y_pred = clf.predict(x_test)

		for idx in range(len(y_pred)):
			y_preds[ test_indices[idx] ].append(y_pred[idx])

		# keep important values for next iteration
		clfs.append(clf)

	# calculate a baseline
	median = [metrics.median(y)] * n_size
	base = sk_metrics.mean_absolute_error(y, median)

	# calculate as median of predictions
	y_ensemble = np.zeros((3, n_size))

	for idx in range(n_size):
		# get the predicted value (the median) 
		y_ensemble[0][idx] = np.mean( y_preds[idx] )

		# get the lower and upper limits of the confidence interval
		lower, upper = metrics.c_interval( y_preds[idx], y_ensemble[0][idx] )

		# save these values
		y_ensemble[1][idx] = lower
		y_ensemble[2][idx] = upper

	# calculate comparators
	comparators = metrics.get_comparators(y, y_ensemble)

	return clfs, comparators, [base, comparators['mean-absolute-error']]

def update_model(model_type, parameter):
	clfs, comparators, accuracy = create_model(model_type, parameter)
	save.update("model", [clfs, model_type, parameter, comparators])
	return accuracy

def get_models(trans):
	prefix = save.get_prefix("model")
	versions = save.get_version(prefix)
	models = []

	for v in range(versions-1):
		_, model_type, parameter, _ = save.load("model", v+1)
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
		_, model_type, parameter, comparators = save.load("model", v+1)
		display.append([model_type, parameter, comparators])

	return display

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

def pad(parameter, defaults):
	split = parameter.split(',')
	while len(split) < len(defaults):
		split.append("")
	for i in range(len(defaults)):
		split[i] = split[i].strip()
		split[i] = split[i].rstrip()
		if split[i] == "":
			split[i] = defaults[i]
	return split

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

def nearest_neighbor(parameter):
	# [ n_neigbors, weights, p, algorithm ] 
	defaults = [5, 'uniform', 2, 'auto']

	split = pad(parameter, defaults)

	return neighbors.KNeighborsRegressor(n_neighbors=int(split[0]), weights=split[1], p=int(split[2]), algorithm=split[3])

def decision_tree(parameter):
	# [ criterion, splitter, max_depth, min_samples_split, min_samples_leaf, max_features]
	defaults = ['mse', 'random', None, 2, 1, None]

	split = pad(parameter, defaults)

	return tree.DecisionTreeRegressor(criterion=split[0], splitter=split[1], max_depth=split[2],
		min_samples_split=split[3], min_samples_leaf=split[4], max_features=split[5])

def boosting(parameter):
	defaults = ['ls', 0.1, 100]
	split = pad(parameter, defaults)
	return ensemble.GradientBoostingRegressor(loss=split[0])

def tsn(parameter):
	return linear_model.TheilSenRegressor()

def k_ridge(parameter):
	return kernel_ridge.KernelRidge

def support_vector(parameter):
	return svm.SVR()

def stochastic(parameter):
	return linear_model.SGDRegressor()


''' UNUSED ML MODELS '''
def mlpregressor(parameter):
	return neural_network.MLPRegressor()

def gpr(parameter):
	return gaussian_process.GaussianProcessRegressor()

def perceptron(parameter):
	return linear_model.Perceptron()