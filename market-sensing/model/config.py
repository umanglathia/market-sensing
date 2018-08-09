input_file = "model/training_data.csv"

parameters = ['program_number', 'use', 'customer', 'engine', 'market_segment', 'market', 'module',
		'tube_type', 'num_tubes', 'length', 'width', 'height', 'mass', 'bypass_valve',
		'num_brackets', 'spigot_type', 'casted flange', 'num_gasboxes', 'peak_volume',
		'lifetime_volume', 'sop_year', 'bw_quote', 'status', 'final_price']

numerical = ['num_tubes', 'length', 'width', 'height', 'mass', 'num_brackets', 'num_gasboxes',
		'peak_volume', 'lifetime_volume', 'sop_year']

features_used = ['customer', 'market_segment', 'market', 'module', 'tube_type', 'num_tubes', 'length',
		'width', 'height', 'mass', 'bypass_valve', 'num_brackets', 'spigot_type', 'num_gasboxes', 
		'peak_volume', 'sop_year']