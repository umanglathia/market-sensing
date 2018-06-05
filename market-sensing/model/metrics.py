def get_accuracy(y_true, y_pred):
	sum_diff = 0.0
	for i in range(len(y_true)):
		sum_diff += abs(y_true[i] - y_pred[i])

	return sum_diff/len(y_true)