from __future__ import print_function
from flask import Flask, render_template, redirect, request
import dill as pickle
from sklearn import linear_model
import sys
import model.machine_learning as machine_learning
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)
all_features =  ["use", "year", "customer", "number of tubes", "length", "width", "height", "mass", "number of gas boxes", "peak volume", "lifetime volume", "final price"]
features_used = ["number of tubes", "length", "width", "height", "mass", "customer", "peak volume", "lifetime volume", "year"]

@app.route("/")
def main():
	acc = None
	return render_template('index.html', **locals())

@app.route("/clean", methods=['GET'])
def clean():
	machine_learning.clean()
	return redirect('/')

@app.route("/update", methods=['GET'])
def update():
	acc = machine_learning.update()
	return render_template('update.html', **locals())

@app.route("/model")
def model():
	return render_template('initial_search.html', **locals())

@app.route("/predict", methods=['POST'])
def predict():	
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

	quote = machine_learning.get_quote(inputs, features_used)
	similar_list = machine_learning.get_similar_list(inputs, features_used)

	return render_template('search.html', **locals())


if __name__ == "__main__":
	app.run()