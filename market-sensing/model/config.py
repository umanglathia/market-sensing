# location of the file used for the training data for the machine learning model
input_file = "model/training_data.csv"

# this should match up one-to-one with the csv used for the training data. if an feature is 
# added or removed in the excel file, it needs to be added or removed here
parameters = ['program_number', 'use', 'customer', 'engine', 'market_segment', 'market', 'module',
		'tube_type', 'num_tubes', 'length', 'width', 'height', 'mass', 'bypass_valve',
		'num_brackets', 'spigot_type', 'casted flange', 'num_gasboxes', 'peak_volume',
		'lifetime_volume', 'sop_year', 'bw_quote', 'status', 'final_price']

# these are the features above that are numerical, meaning that they are numbers AND they
# can be compared to each other with < and > symbols in their semantic meaning
numerical = ['num_tubes', 'length', 'width', 'height', 'mass', 'num_brackets', 'num_gasboxes',
		'peak_volume', 'lifetime_volume', 'sop_year']

# these are the features that are used for the machine learning model. any of those that are in
# 'parameters' object can be used here
features_used = ['customer', 'market_segment', 'market', 'module', 'tube_type', 'num_tubes', 'length',
		'width', 'height', 'mass', 'bypass_valve', 'num_brackets', 'spigot_type', 'num_gasboxes', 
		'peak_volume', 'sop_year']