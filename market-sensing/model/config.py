input_file = "model/test_data.csv"

parameters = ['program_number', 'use', 'num_tubes', "tube_type", 'length', 'width', 'height', 'mass',
		'bypass_valve', 'num_brackets', 'spigot_type', 'num_gasboxes', 'peak_volume', 'lifetime_volume',
		'customer', 'market_segment', 'market', 'sop_year', 'bw_quote', 'status', 'final_price']

numerical = ['num_tubes', 'length', 'width', 'height', 'mass', 'num_brackets', 'num_gasboxes',
		'peak_volume', 'lifetime_volume', 'sop_year']

features_used = ["num_tubes", "tube_type", "length", "width", "height", 'mass', 'peak_volume',
		"lifetime_volume", 'customer', 'market', 'sop_year']