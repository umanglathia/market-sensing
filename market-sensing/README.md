# market-sensing

CRAETED:
Created by Umang Lathia during Summer 2018 for a Tauber Summer Project, specifcially the BorgWarner Market Sensing Project.

FUNCTIONALITY:
This is a project developed by the Tauber Team from the University of Michigan. It is used to predict the market value of EGR coolers based on previous historical bids using a two-tier machine learning model. It also returns examples of similar historical coolers based on a custom-written KNN algorithm that includes weighting determined by the BorgWarner team.  

REQUIREMENTS:
Uses Python3.6
Before this application will work, you will need to use the command 'pip install' to install the following:
	 - wtforms
	 - flask
	 - dill
	 - numpy
	 - sklearn
	 - scipy

FILES:
app.py - The main router for this application and the one that provides the interface layer. Use the command 'python app.py' to begin running this application once it is downloaded and the requirements are fulfilled

MODEL FILES:
	config.py - This file contains some of the key objects that are used by many different parts of this program. Specifically, to change the location of the machine learning data, to change the parameters in the CSV file that are read in, or to change the interaction of those parameters, use this file.

	data_input.py - This file converts the CSV data into a Python object and cleans the values for comparison. It also provides the interface to add a sample to the data.

	features.py - This file controls the creation of a samples suitiable for machine learning from the data that is input. If there was custom parameter manipulation to be achieved, this is the file where this is possible.

	machine_learning.py - The core interface between the backend and the front end, this file handles requests from app.py and calls the appropriate other functions to satisfy these request.

	metrics.py - This file calculates the key metrics that were used to evaluate the machine learning models used in this project.

	ml_models.py - This file contains the machine learning models that are used for this project. They are called using an indirect interface in machine_learning. Parameters are provided by the web interface and must be provided in the exact order for those parameters to be accepted.

	results.py - This file is called by machine_learning and runs the prediction and formats the output correctly to be viewed on the web interface.

	save.py - This file is called by machine_learning and updates the versions of the model and data that are saved for easier future use. It uses a python library called dill to accomplish this.

	similarity.py - This file is called my machine_learning and runs the similarity algorithms that are used for the secondary outputs. The algorithm is baed on KNN, and has implementations for manhattan, eucledian, and cosine distance. The eucledian distance is used for this algorithm.

