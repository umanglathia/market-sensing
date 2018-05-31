from __future__ import print_function
from flask import Flask, render_template, redirect, request
import dill as pickle
from sklearn import linear_model
import sys
import model.machine_learning as machine_learning
from model.data_input import parameters
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)
features_used = ["number of tubes", "length", "width", "height", "mass", "customer", "peak volume", "lifetime volume", "sop year"]


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
	acc1, acc2 = machine_learning.update()
	print("Accuracy: " + str(acc2))
	return render_template('update.html', **locals())

@app.route("/model")
def model():
	return render_template('initial_search.html', **locals())

@app.route("/predict", methods=['POST'])
def predict():
	form = request.form
	
	program_dict = {}

	for attr in parameters:
		program_dict[attr] = form.get(attr, "")

	quote = machine_learning.get_quote(program_dict, features_used)
	similar_list = [1, 2, 3]
	#machine_learning.get_similar_list(inputs, features_used)

	return render_template('search.html', **locals())


if __name__ == "__main__":
	app.run()