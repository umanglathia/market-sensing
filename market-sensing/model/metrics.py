import numpy as np
import sklearn.metrics as sk_metrics
import scipy.stats as st
import math

# calculate the mean percentage error between the prediction and the true value
def mean_percentage_error(y_true, y_pred):
	summation = 0
	for i in range(len(y_true)):
		summation += abs(y_true[i] - y_pred[i])/y_true[i]

	return float(summation/len(y_true))*100

# calculate the accuracy that the prediction falls in the confidence interval
def ci_accuracy(y, lowers, uppers):
	correct = 0.0
	total = 0.0

	for idx in range(len(y)):
		if y[idx] >= lowers[idx] and y[idx] <= uppers[idx]:
			correct += 1.0
		total += 1.0

	return correct/total*100

# calculate the average confidence interval size
def mean_ci_range(lowers, uppers):
	return np.mean(uppers - lowers)

def get_comparators(y, y_ensemble):
	comparators = {}
	comparators['mean-absolute-error'] = sk_metrics.mean_absolute_error(y, y_ensemble[0])
	comparators['root-mean-square-error'] = math.sqrt(sk_metrics.mean_squared_error(y, y_ensemble[0]))
	comparators['mean-percent-error'] = mean_percentage_error(y, y_ensemble[0])
	comparators['median-absolute-error'] = sk_metrics.median_absolute_error(y, y_ensemble[0])
	comparators['ci-accuracy'] = ci_accuracy(y, y_ensemble[1], y_ensemble[2])
	comparators['mean-ci-range'] = mean_ci_range(y_ensemble[1], y_ensemble[2])

	return comparators

def c_interval(values, mean, alpha = 0.95):
	p = (1.0 - alpha)/2.0
	z = st.norm.ppf(1 - p)
	sigma = np.std(values)
	return mean - z*sigma, mean + z*sigma 

def median(values):
	if len(values) == 0:
		return 0.0
	return np.percentile(values, 50)