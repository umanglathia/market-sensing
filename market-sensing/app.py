from __future__ import print_function
from flask import Flask, render_template, redirect, request, session
from wtforms import Form, TextField, IntegerField, SubmitField, SelectField, validators, FloatField
from sklearn import linear_model
import sys
import model.machine_learning as machine_learning
from model.data_input import parameters

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'

class ModelForm(Form):
	num_tubes = IntegerField("# of Tubes",
		[validators.optional()])
	tube_type = SelectField("Type of Tube",
		choices=[(' ', ' '), ('Corrugate', 'Corrugate'), ('Hybrid', 'Hybrid')])
	length = FloatField("Length (mm)",
		[validators.optional()])
	width = FloatField("Width (mm)",
		[validators.optional()])
	height = FloatField("Height (mm)",
		[validators.optional()])
	mass = FloatField("Mass (g) ",
		[validators.optional()])
	bypass_valve = SelectField("Bypass Valve",
		choices=[(' ', ' '), ('Yes', 'Yes'), ('No', 'No')])
	num_brackets = IntegerField("# of Brackets",
		[validators.optional()])
	spigot_type = SelectField("Type of Spigot",
		choices=[(' ', ' '), ('Straight', 'Straight'), ('Bend', 'Bend')])
	num_gasboxes = IntegerField("# of Gas Boxes",
		[validators.optional()])
	peak_volume = IntegerField("Peak Volume",
		[validators.optional()])
	lifetime_volume = IntegerField("Lifetime Volume",
		[validators.optional()])
	customer = SelectField("Customer",
		choices=[(' ', ' '), ('Ford', 'Ford'), ('Nissan', 'Nissan'), ('GM', 'GM'),
		('HKMC', 'HKMC'), ('FCA', 'FCA'), ('Mitsubishi', 'Mitsubishi'), ('Maruti', 'Maruti'),
		('VCC', 'VCC')])
	car_type = SelectField("Car Type",
		choices=[(' ', ' '), ('Passenger', 'Passenger'), ('Commercial', 'Commercial')])
	region = SelectField("Region",
		choices=[(' ', ' '), ('EU', 'EU'), ('North America', 'North America'),
		('South America', 'South America'), ('Asia', 'Asia')])
	sop_year = IntegerField("SOP Year",
		[validators.optional()])

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
	return render_template('update.html', **locals())

@app.route("/model")
def model():
	form = ModelForm(request.form)
	return render_template('form.html', **locals())


@app.route("/predict", methods=['POST'])
def predict():
	form = ModelForm(request.form)
	input_form = request.form
	if request.method == 'POST' and form.validate():
		program = {}

		for attr in parameters:
			program[attr] = input_form.get(attr, "")

		quote, similar_list = machine_learning.predict_cooler(program)
		return render_template('results.html', **locals())

	return render_template('form.html', **locals())

if __name__ == "__main__":
	app.run()