import os
import dill as pickle
from sklearn import linear_model, svm

def clean():
	filename_to_delete = ""
	current_filename = "models/model_v1.pk"
	current_filename2 = "models/data_v1.pk"
	version = 1
	complete = False
	
	while not complete:
		version += 1
		temp_filename = "models/model_v" + str(version) + ".pk"
		temp_filename2 = "models/data_v" + str(version) + ".pk"

		if os.path.exists(temp_filename):
			os.remove(current_filename)
			os.remove(current_filename2)
			current_filename = temp_filename
			current_filename2 = temp_filename2
		
		else:
			os.rename(current_filename, "models/model_v1.pk")
			os.rename(current_filename2, "models/data_v1.pk")
			complete = True

	return


def update(clf, programs, accuracy):
	version = 1
	found = False
	while not found:
		filename = "models/model_v" + str(version) + ".pk"
		data_file = "models/data_v" + str(version) + ".pk"
		if not os.path.exists(filename):
			found = True

		version += 1

	with open(filename, "wb") as file:
		pickle.dump(clf, file)

	with open(data_file, "wb") as file:
		pickle.dump(programs, file)

	return accuracy


def load_latest_model():
	version = 1
	filename = "models/model_v1.pk"
	filename2 = "models/data_v1.pk"
	while True:
		version += 1
		temp_filename = "models/model_v" + str(version) + ".pk"
		temp_filename2 = "models/data_v" + str(version) + ".pk"
		if os.path.exists(temp_filename):
			filename = temp_filename
			filename2 = temp_filename2
		else:
			with open(filename, "rb") as f:
				clf = pickle.load(f)
				with open(filename2, "rb") as f2:
					data = pickle.load(f2)
					return clf, data