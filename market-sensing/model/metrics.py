import numpy as np
import sklearn.metrics as sk_metrics
import math

def mean_percentage_error(y_true, y_pred):
	summation = 0
	for i in range(len(y_true)):
		summation += abs(y_true[i] - y_pred[i])/y_true[i]

	return float(summation/len(y_true))*100

def get_comparators(y, y_pred_ensemble):
	comparators = {}
	comparators['mean-absolute-error'] = sk_metrics.mean_absolute_error(y, y_pred_ensemble)
	comparators['root-mean-square-error'] = math.sqrt(sk_metrics.mean_squared_error(y, y_pred_ensemble))
	comparators['mean-percent-error'] = mean_percentage_error(y, y_pred_ensemble)
	comparators['median-absolute-error'] = sk_metrics.median_absolute_error(y, y_pred_ensemble)

	return comparators

def c_interval(values, alpha = 0.95):
	p = (1.0 - alpha)/2.0 * 100
	return max(np.percentile(values, p), 0.0), max(np.percentile(values, 100-p), 0.0)

def median(values):
	if len(values) == 0:
		return 0.0
	return np.percentile(values, 50)