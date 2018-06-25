import numpy as np

def get_accuracy(y_true, y_pred):
	sum_diff = 0.0
	for i in range(len(y_true)):
		sum_diff += abs(y_true[i] - y_pred[i])

	return sum_diff/len(y_true)

def c_interval(values, alpha = 0.95):
	p = (1.0 - alpha)/2.0 * 100
	return max(np.percentile(values, p), 0.0), max(np.percentile(values, 100-p), 0.0)

def median(values):
	return np.percentile(values, 50)