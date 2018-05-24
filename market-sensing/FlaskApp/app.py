from __future__ import print_function
from flask import Flask, render_template, redirect, request
import dill as pickle
from sklearn import linear_model
import sys
sys.path.append('C:\\Users\\ulathia\\Documents\\project\\FlaskApp\\model')
import data_input
import model as umang
import main

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html', **locals())

@app.route("/begin", methods=['POST'])
def begin():
	return redirect('/parameters')

@app.route("/parameters")
def parameters():
	return render_template('parameters.html')

@app.route("/create", methods=['POST'])
def create():
	
	return redirect('/model')

@app.route("/model")
def model():
	return render_template('model.html', **locals())

@app.route("/predict", methods=['POST'])
def predict():


	
	filename = "model_v2.pk"
	with open("models/"+filename, "rb") as f:
		clf = pickle.load(f)


	all_features =  ["use", "year", "customer", "number of tubes", "length", "width", "height", "mass", "number of gas boxes", "peak volume", "lifetime volume", "final price"]
	features_used = ["number of tubes", "length", "width", "height", "mass", "customer", "peak volume", "lifetime volume", "year"]

	inputs = [""]*len(all_features)

	inputs[1] = request.form.get('year', "")
	inputs[2] = request.form.get('customer', "")
	inputs[3] = request.form.get('num_tubes', "")
	inputs[4] = request.form.get('length', "")
	inputs[5] = request.form.get('width', "")
	inputs[6] = request.form.get('height', "")
	inputs[7] = request.form.get('mass', "")
	inputs[9] = request.form.get('peak-volume', "")
	inputs[10] = request.form.get('lifetime-volume', "")

	cooler = data_input.create_program(inputs)
	x, y = umang.features_labels([cooler], features_used)
	quote = clf.predict(x)[0]

	return str(quote)


if __name__ == "__main__":
	app.run()