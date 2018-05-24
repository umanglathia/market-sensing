def accuracy(y_true, y_pred, threshold=0.5):
	numerator = 0
	denominator = 0
	for i in range(len(y_true)):
		if y_pred[i] > threshold:
			pred = 1
		elif y_pred[i] <= threshold:
			pred = 0
		if y_true[i] == pred:
			numerator += 1
		denominator += 1

	return numerator/denominator