from sklearn import linear_model, svm, neighbors, tree, ensemble, neural_network, kernel_ridge

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