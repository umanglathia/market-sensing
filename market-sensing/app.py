from __future__ import print_function
from flask import Flask, render_template, redirect, request, session, url_for
from wtforms import Form, RadioField, IntegerField, SubmitField, SelectField, validators, FloatField, TextField
from sklearn import linear_model
import sys
import model.machine_learning as machine_learning
from model.data_input import parameters

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'

trans = {
	"least_squares": "Least Squares",
	"ridge": "Ridge",
	"lasso": "Lasso",
	"elastic_net": "Elastic Net",
	"lasso_lars": "Lasso LARS",
	"nearest_neighbor": "Nearest Neighbor",
	"decision_tree": "Decision Tree",
	"boosting": "Boosting",
	"tsn": "Theil Sen Regressor",
	"k_ridge": "Kernel Ridge",
	"support_vector": "Support Vector Machine",
	"stochastic": "Stochastic Gradient Descent"
}

global_metrics = {
	"mean-absolute-error": "Mean Absolute Error",
	"root-mean-square-error": "Root Mean Square Error",
	"mean-percent-error": "Mean Percent Error",
	"median-absolute-error": "Median Absolute Error",
	"ci-accuracy": "Confidence Interval Accuracy",
	"mean-ci-range": "Mean Confidence Interval Range"
}

class NonValidatingSelectField(SelectField):
    """
    Attempt to make an open ended select  field that can accept dynamic
    choices added by the browser.
    """
    def pre_validate(self, form):
        pass

class ModelForm(Form):
	num_tubes = IntegerField("# of Tubes",
		[validators.optional()])
	tube_type = SelectField("Tube Type",
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
		choices=[(' ', ' '), ('BAIC', 'BAIC'), ('BMW', 'BMW'), ('CNH Global', 'CHN Global'), ('DAE', 'DAE'),
		('Daimler Truck', 'Daimler Truck'), ('Deutz', 'Deutz'), ('DFL', 'DFL'), ('FCA', 'FCA'),
		('Ford', 'Ford'), ('Foton', 'Foton'), ('GAC', 'GAC'), ('GM', 'GM'), ('HKMC', 'HKMC'),
		('HMC', 'HMC'), ('JAC', 'JAC'), ('JLR', 'JLR'),	('JMC', 'JMC'), ('Liebherr', 'Liebherr'),
		('MAN', 'MAN'), ('Maruti', 'Maruti'), ('Mitsubishi', 'Mitsubishi'),
		('NAVECO', 'NAVECO'), ('Nissan', 'Nissan'),	('Renault', 'Renault'), ('Subaru', 'Subaru'),
		('VCC', 'VCC'), ('Volvo', 'Volvo'), ('Yuchai', 'Yuchai')])
	market_segment = SelectField("Market Segment",
		choices=[(' ', ' '), ('Passenger', 'Passenger'), ('Commercial', 'Commercial')])
	market = SelectField("Region",
		choices=[(' ', ' '), ('EU', 'EU'), ('North America', 'North America'),
		('South America', 'South America'), ('Asia', 'Asia')])
	sop_year = IntegerField("SOP Year",
		[validators.optional()])
	sim_model = SelectField("Similarity Model", 
		choices=[('euclidean','Euclidean'),('manhattan','Manhattan'), ('cosine', 'Cosine')])
	num_results = SelectField("Results",
		choices=[('5', '5'),('10', '10')])
	pred_model = SelectField("Prediction Model",
		choices=[])


class TestingForm(Form):
	model_type = SelectField('Model Type',
		choices= [(key, trans[key]) for key in trans.keys()])
	parameter = TextField("Parameter")

@app.route("/")
def main():
	acc = None
	return render_template('index.html', **locals())

@app.route("/test", methods=['GET'])
def redirecter():
	return redirect(url_for('test', action="index"))

@app.route("/test/", methods=['GET'])
def redirecter2():
	return redirecter()

@app.route("/test/<action>", methods=['GET', 'POST'])
def test(action):
	form = TestingForm(request.form)

	if request.method == 'GET':

		if action == "index":
			return render_template('test.html', **locals())

		if action == "create":
			return render_template('create.html', **locals())	

		if action == "run":
			results = machine_learning.run()
			for i in range(len(results)):
				results[i][0] = trans[ results[i][0] ]

			metrics = global_metrics
			return render_template('run.html', **locals())

		if action == "data":
			machine_learning.clean()
			machine_learning.update_data()
			return render_template('update_data.html', **locals())

	if request.method == 'POST' and action == 'create':
		model_type = form.model_type.data
		parameter = form.parameter.data
		base, error = machine_learning.create(model_type, parameter)
		return render_template('created.html', **locals())

@app.route("/add", methods=['GET', 'POST'])
def add():
	form = ModelForm(request.form)
	
	if request.method == 'GET':
		return render_template('add.html', **locals())

	if request.method == 'POST':
		input_form = request.form
		program = {}

		for attr in parameters:
			program[attr] = input_form.get(attr, '')

		success = machine_learning.add_cooler(program)

		if success == "SUCCESS":
			return render_template('added.html', **locals())

@app.route("/remove", methods=['GET', 'POST'])
def remove():
	if request.method == 'GET':	
		return render_template('remove.html', **locals())

	if request.method == 'POST':
		return render_template('removed.html', **locals())

@app.route("/model", methods=['GET', 'POST'])
def model():
	form = ModelForm(request.form)
	models = machine_learning.get_models(trans)
	form.pred_model.choices = [(c['id'], c['name']) for c in models]

	if request.method == 'GET':
		return render_template('form.html', **locals())

	if request.method == 'POST': 
		input_form = request.form
		program = {}

		for attr in parameters:
			program[attr] = input_form.get(attr, '')

		program['module'] = "No"

		'''
		s = input_form.get('sim_model', '')
		r = int(input_form.get('num_results', ''))
		p = input_form.get('pred_model', '')
		'''
		s = "euclidean"
		r = 5

		quote, lower, upper, similar_list = machine_learning.predict(program, s, r)

		return render_template('results.html', **locals())

if __name__ == "__main__":
	app.run()